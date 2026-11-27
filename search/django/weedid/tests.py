"""Regression tests for the Nov 2026 Wiz Red Agent findings.

Run inside the django container:
    docker compose exec django python manage.py test weedid
"""
import json
from unittest import mock

from django.test import TestCase

from weedid.models import Dataset, WeedidUser
from weedid.views import GOOGLE_CLIENT_ID


def _tokeninfo(status=200, **claims):
    base = {
        "aud": GOOGLE_CLIENT_ID,
        "iss": "https://accounts.google.com",
        "email": "researcher@example.org",
        "email_verified": "true",
        "sub": "1234567890",
    }
    base.update(claims)
    resp = mock.Mock(status_code=status)
    resp.json.return_value = base
    return resp


class GoogleLoginTests(TestCase):
    """Finding 1: /api/login_google/ must not trust client-supplied identity."""

    url = "/api/login_google/"

    def post(self, payload):
        return self.client.post(
            self.url, json.dumps(payload), content_type="application/json"
        )

    def assertNotLoggedIn(self):
        self.assertEqual(self.client.get("/api/login_status/").status_code, 403)

    def test_wiz_payload_rejected(self):
        WeedidUser.objects.create_user("victim", "victim@example.org", "pw")
        with mock.patch("weedid.views.requests.get") as get:
            resp = self.post({"email": "victim@example.org", "googleId": "999999"})
        self.assertEqual(resp.status_code, 403)
        get.assert_not_called()
        self.assertNotLoggedIn()

    def test_invalid_token_rejected(self):
        with mock.patch("weedid.views.requests.get", return_value=_tokeninfo(400)):
            self.assertEqual(self.post({"credential": "x"}).status_code, 403)
        self.assertNotLoggedIn()

    def test_wrong_audience_rejected(self):
        with mock.patch(
            "weedid.views.requests.get", return_value=_tokeninfo(aud="other-app")
        ):
            self.assertEqual(self.post({"credential": "x"}).status_code, 403)
        self.assertNotLoggedIn()

    def test_wrong_issuer_rejected(self):
        with mock.patch(
            "weedid.views.requests.get", return_value=_tokeninfo(iss="evil.com")
        ):
            self.assertEqual(self.post({"credential": "x"}).status_code, 403)

    def test_unverified_email_rejected(self):
        with mock.patch(
            "weedid.views.requests.get", return_value=_tokeninfo(email_verified="false")
        ):
            self.assertEqual(self.post({"credential": "x"}).status_code, 403)
        self.assertNotLoggedIn()

    def test_identity_comes_from_token_not_body(self):
        WeedidUser.objects.create_user("victim", "victim@example.org", "pw")
        with mock.patch("weedid.views.requests.get", return_value=_tokeninfo()):
            resp = self.post(
                {"credential": "x", "email": "victim@example.org", "googleId": "1"}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            WeedidUser.objects.get(email="researcher@example.org").id,
        )

    def test_existing_user_logged_in(self):
        user = WeedidUser.objects.create_user("r", "researcher@example.org", "pw")
        with mock.patch("weedid.views.requests.get", return_value=_tokeninfo()):
            self.assertEqual(self.post({"credential": "x"}).status_code, 200)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id)

    def test_new_google_user_has_no_usable_password(self):
        with mock.patch("weedid.views.requests.get", return_value=_tokeninfo()):
            self.assertEqual(self.post({"credential": "x"}).status_code, 200)
        user = WeedidUser.objects.get(email="researcher@example.org")
        self.assertFalse(user.has_usable_password())


class PasswordLoginTests(TestCase):
    """Finding 1 (related): the stored hash must not work as a password."""

    def setUp(self):
        self.user = WeedidUser.objects.create_user("alice", "a@example.org", "s3cret!")

    def login(self, password):
        return self.client.post(
            "/api/login/", {"username": "alice", "password": password}
        )

    def test_correct_password(self):
        self.assertEqual(self.login("s3cret!").status_code, 200)

    def test_hash_is_not_a_password(self):
        self.assertEqual(self.login(self.user.password).status_code, 400)


class UploadInfoTests(TestCase):
    """Finding 2: no contributor emails from the public metadata API."""

    def setUp(self):
        Dataset.objects.create(
            upload_id="21675efe-9d25-4096-be76-3a541475efd4",
            status="C",
            metadata={
                "name": "Test",
                "creator": [
                    {
                        "name": "A B",
                        "email": "someone@gmail.com",
                        "affiliation": {"name": "USyd", "email": "x@y.z"},
                    }
                ],
            },
        )

    def test_emails_redacted(self):
        resp = self.client.get("/api/upload_info/21675efe-9d25-4096-be76-3a541475efd4")
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn("@", resp.content.decode())
        creator = json.loads(resp.content)["metadata"]["creator"][0]
        self.assertEqual(creator["name"], "A B")
        self.assertEqual(creator["affiliation"], {"name": "USyd"})

    def test_unknown_dataset_404(self):
        self.assertEqual(self.client.get("/api/upload_info/nope").status_code, 404)


class ElasticsearchProxyTests(TestCase):
    """Finding 3: proxy is pinned to weedid/_msearch and rejects scripts."""

    url = "/elasticsearch/weedid/_msearch"

    def post(self, body, url=None):
        return self.client.post(
            url or self.url, body, content_type="application/x-ndjson"
        )

    def _es_ok(self):
        resp = mock.Mock(status_code=200, content=b'{"responses":[]}')
        return resp

    def test_plain_search_forwarded_and_index_pinned(self):
        body = '{"preference":"r","index":"_all"}\n{"query":{"match_all":{}}}\n'
        with mock.patch("weedid.views.requests.post", return_value=self._es_ok()) as p:
            resp = self.post(body)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(p.call_args[1]["url"].endswith("/weedid/_msearch"))
        sent = p.call_args[1]["data"].decode().splitlines()
        self.assertEqual(json.loads(sent[0]), {"preference": "r"})
        self.assertNotIn("Cookie", p.call_args[1]["headers"])

    def test_script_fields_rejected(self):
        body = (
            "{}\n"
            '{"size":1,"script_fields":{"t":{"script":{"source":"return 77"}}}}\n'
        )
        with mock.patch("weedid.views.requests.post") as p:
            self.assertEqual(self.post(body).status_code, 400)
        p.assert_not_called()

    def test_nested_script_query_rejected(self):
        body = '{}\n{"query":{"bool":{"filter":[{"script":{"script":"1"}}]}}}\n'
        with mock.patch("weedid.views.requests.post") as p:
            self.assertEqual(self.post(body).status_code, 400)
        p.assert_not_called()

    def test_other_paths_rejected(self):
        with mock.patch("weedid.views.requests.post") as p:
            for url in ["/elasticsearch/_all/_msearch", "/elasticsearch/weedid/_search"]:
                self.assertEqual(self.post("{}\n{}\n", url).status_code, 400)
        p.assert_not_called()

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_malformed_body_rejected(self):
        with mock.patch("weedid.views.requests.post") as p:
            self.assertEqual(self.post("not json\n{}\n").status_code, 400)
            self.assertEqual(self.post("{}\n").status_code, 400)
        p.assert_not_called()
