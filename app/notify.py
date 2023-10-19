from notifications_python_client.notifications import NotificationsAPIClient
from config import Config
import logging
from models.email import Email


logger = logging.getLogger("uvicorn")

notifications_client = NotificationsAPIClient(Config.GOVUK_NOTIFY_API_KEY)


def send_email(email: Email):
    response = notifications_client.send_email_notification(
        email_address=email.email_address,  # required string
        template_id=email.template_id,  # required UUID string
        personalisation=email.personalisation,  # optional dictionary
    )
    return response
