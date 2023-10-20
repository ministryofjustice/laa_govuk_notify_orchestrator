from notifications_python_client.notifications import NotificationsAPIClient
from config import Config
import logging


logger = logging.getLogger("uvicorn")

notifications_client = NotificationsAPIClient(Config.GOVUK_NOTIFY_API_KEY)


def send_email(email_address: str, template_id: str, personalisation: dict):
    response = notifications_client.send_email_notification(
        email_address=email_address,  # required string
        template_id=template_id,  # required UUID string
        personalisation=personalisation,  # optional dictionary
    )
    return response
