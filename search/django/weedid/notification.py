import logging
from textwrap import dedent

from core.settings import DEBUG, SITE_BASE_URL

from weedid.models import Dataset, WeedidUser
from weedid.utils import send_email

logger = logging.getLogger(__name__)


def upload_notification(upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    uploader = upload_entity.user
    email_body = f"""\
    User {uploader.username} <{uploader.email}> has uploaded a dataset {upload_entity.metadata['name']} to review.
    {'Please review it now by accessing the dataset here: ' + SITE_BASE_URL + '/datasets/' + upload_id}.
    """
    staff_recipients = [
        staff.email for staff in WeedidUser.objects.filter(is_staff=True)
    ]
    if DEBUG:
        logger.info(email_body)
    else:
        send_email(
            f"New upload ({upload_entity.metadata['name']})",
            dedent(email_body),
            staff_recipients,
        )


def review_notification(message, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    uploader = upload_entity.user
    email_body = f"""\
    Dear {uploader.username},

    Many thanks for contributing to a growing community and repository of weed image datasets.

    Your dataset upload {upload_entity.metadata['name']} has been {message} after review.

    {'Congratulations! You can now view the entire dataset online from ' + SITE_BASE_URL + '/datasets/' + upload_id if 'approved' in message else 'Unfortunately at this stage your dataset has not been approved. Please contact weed-ai.app@sydney.edu.au for further information.'}.

    Regards,
    Weed-AI Team
    """
    if DEBUG:
        logger.info(email_body)
    else:
        send_email(
            f"Your upload ({upload_entity.metadata['name']}) has been {message}",
            dedent(email_body),
            [uploader.email],
        )


def edit_notification(message, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    uploader = upload_entity.user
    email_body = f"""\
    Dear {uploader.username},

    Many thanks for contributing to a growing community and repository of weed image datasets.

    Your edit on dataset {upload_entity.metadata['name']} has been {message}.

    {'Congratulations! You can now view the latest version of it online from ' + SITE_BASE_URL + '/datasets/' + upload_id if message == 'successful' else 'Your dataset will remain as the previous version and please contact weed-ai.app@sydney.edu.au for further information if you still want to edit it.'}.

    Regards,
    Weed-AI Team
    """
    if DEBUG:
        logger.info(email_body)
    else:
        send_email(
            f"Your upload ({upload_entity.metadata['name']}) has been {message}",
            dedent(email_body),
            [uploader.email],
        )
