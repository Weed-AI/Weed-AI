#!/usr/bin/env bash
# Black-box checks for the Nov 2026 Wiz findings, run against a deployed stack.
#   Local:  ./scripts/check_wiz_fixes.sh http://localhost
#   Prod:   ./scripts/check_wiz_fixes.sh https://weed-ai.sydney.edu.au
# Optional: ES_URL=http://localhost:9200 (local only) to also check ES directly.
set -u
BASE="${1:-http://localhost}"; BASE="${BASE%/}"
ES_URL="${ES_URL:-}"
JAR=$(mktemp); trap 'rm -f "$JAR" /tmp/wiz_body' EXIT
pass=0; fail=0
ok()  { echo "  PASS  $1"; pass=$((pass+1)); }
bad() { echo "  FAIL  $1"; fail=$((fail+1)); }
expect() { # name expected actual
  if [ "$2" = "$3" ]; then ok "$1 ($3)"; else bad "$1 (expected $2, got $3)"; fi; }
req() { curl -sk -o /tmp/wiz_body -w '%{http_code}' -b "$JAR" -c "$JAR" -H "Referer: $BASE/" "$@"; }

# Fresh local stacks have no weedid index; create an empty one so the proxy
# checks below aren't confused by index_not_found.
[ -n "$ES_URL" ] && curl -s -XPUT "$ES_URL/weedid" >/dev/null

curl -sk -c "$JAR" "$BASE/api/set_csrf/" >/dev/null
CSRF=$(awk '$6=="csrftoken"{print $7}' "$JAR")
[ -n "$CSRF" ] || { echo "Could not get csrftoken from $BASE/api/set_csrf/"; exit 2; }

echo "Finding 1 - Google login bypass"
code=$(req -X POST "$BASE/api/login_google/" -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" -d '{"email":"securitytest@example.com","googleId":"999999"}')
[ "$code" != 200 ] && ok "Wiz payload rejected ($code)" || bad "Wiz payload accepted (200)"
expect "login_status after attempt" 403 "$(req "$BASE/api/login_status/")"
code=$(req -X POST "$BASE/api//login_google/" -H "Content-Type: application/json" -H "X-CSRFToken: $CSRF" -d '{}')
[ "$code" != 200 ] && ok "double-slash variant rejected ($code)" || bad "double-slash variant 200"

echo "Finding 4 - nginx"
srv=$(curl -skI "$BASE/" | awk -F': ' 'tolower($1)=="server"{print $2}' | tr -d '\r')
case "$srv" in *[0-9]*) bad "Server header leaks version: $srv";; *) ok "Server header: ${srv:-<none>}";; esac
echo "  INFO  version must be checked on the host: docker exec reverse_proxy nginx -v  (want >= 1.30.7)"

echo "Finding 2 - emails in /api/upload_info"
expect "unknown dataset" 404 "$(req "$BASE/api/upload_info/00000000-0000-0000-0000-000000000000")"
ids=$(curl -sk "$BASE/api/upload_list/" | python3 -c 'import sys,json;print("\n".join(d["upload_id"] for d in json.load(sys.stdin)))' 2>/dev/null)
n=0; leaks=0
for id in $ids; do
  n=$((n+1)); curl -sk "$BASE/api/upload_info/$id" | grep -q '"email"' && { leaks=$((leaks+1)); echo "        leak: $id"; }
done
[ "$n" = 0 ] && echo "  INFO  no published datasets to check" || { [ "$leaks" = 0 ] && ok "$n datasets, no email fields" || bad "$leaks/$n datasets expose email"; }

echo "Finding 3 - Elasticsearch proxy"
ES="$BASE/elasticsearch/weedid/_msearch"
H=(-H "Content-Type: application/x-ndjson" -H "X-CSRFToken: $CSRF")
code=$(req -X POST "$ES" "${H[@]}" --data-binary $'{"preference":"t"}\n{"size":0,"query":{"match_all":{}}}\n')
expect "normal search still works" 200 "$code"
code=$(req -X POST "$ES" "${H[@]}" --data-binary $'{}\n{"size":1,"_source":false,"script_fields":{"t":{"script":{"source":"return 77","lang":"painless"}}}}\n')
if grep -q '77' /tmp/wiz_body && [ "$code" = 200 ]; then bad "Painless script executed"; else ok "script_fields blocked ($code)"; fi
code=$(req -X POST "$ES" "${H[@]}" --data-binary $'{"index":"no-such-index-wiz"}\n{"size":0}\n')
if grep -q 'index_not_found' /tmp/wiz_body; then bad "header index override honoured (not pinned)"; else ok "header index override ignored ($code)"; fi
expect "other ES paths" 403 "$(req -X POST "$BASE/elasticsearch/_all/_msearch" "${H[@]}" --data-binary $'{}\n{}\n')"
expect "GET on proxy" 403 "$(req "$ES")"

if [ -n "$ES_URL" ]; then
  echo "Elasticsearch direct (local only)"
  T="$ES_URL/wiz-check"
  curl -s -XPUT "$T/_doc/1?refresh=true" -H 'Content-Type: application/json' -d '{"x":1}' >/dev/null
  out=$(curl -s -XPOST "$T/_search" -H 'Content-Type: application/json' \
        -d '{"size":1,"script_fields":{"t":{"script":"return 77"}}}')
  echo "$out" | grep -q 'cannot execute scripts using \[field\] context' \
    && ok "ES refuses field-context scripts" || bad "ES script_fields not refused: ${out:0:150}"
  out=$(curl -s -XPOST "$T/_update_by_query?conflicts=proceed" -H 'Content-Type: application/json' \
        -d '{"script":{"source":"ctx._source.x = 2"},"query":{"match_all":{}}}')
  echo "$out" | grep -q '"updated":1' && ok "update_by_query scripts still allowed (indexing OK)" \
    || bad "update_by_query broken: ${out:0:150}"
  curl -s -XDELETE "$T" >/dev/null
fi

echo; echo "$pass passed, $fail failed"; [ "$fail" = 0 ]
