from core.settings import SITE_BASE_URL
from weedid.models import Dataset, WeedidUser
from weedid.utils import send_email
from textwrap import dedent


def upload_notification(upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    uploader = upload_entity.user
    email_body = f"""\
    User {uploader.username} <{uploader.email}> has uploaded a dataset {upload_entity.metadata['name']} to review.
    {'You can check it from ' + SITE_BASE_URL + '/datasets/' + upload_id}.
    """
    staff_recipients = [
        staff.email for staff in WeedidUser.objects.filter(is_staff=True)
    ]
    send_email(
        f"New upload ({upload_entity.metadata['name']})",
        dedent(email_body),
        staff_recipients,
    )


def review_notification(message, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    uploader = upload_entity.user
    email_body = f"""\
    Dear Weed-AI contributor,

    Your dataset upload {upload_entity.metadata['name']} has been {message} after review
    {'You can check it from ' + SITE_BASE_URL + '/datasets/' + upload_id if message == 'approved' else 'Feel free to contact our admin'}.

    Regards,
    Weed-AI Team
    """
    send_email(
        f"Your upload ({upload_entity.metadata['name']}) has been {message}",
        dedent(email_body),
        [uploader.email],
    )
