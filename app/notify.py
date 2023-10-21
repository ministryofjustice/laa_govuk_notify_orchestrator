from notifications_python_client.notifications import NotificationsAPIClient
from config import Config
import logging


logger = logging.getLogger("uvicorn")

try:
    notify_client = NotificationsAPIClient(Config.GOVUK_NOTIFY_API_KEY)
except AssertionError as exception:
    if not Config.TESTING_MODE:
        raise exception
    notify_client = None


def send_email(self, email_address: str, template_id: str, personalisation: dict):
    if not notify_client:
        raise EnvironmentError(
            "Notify client has not been created. Please ensure you have a valid Notify API Key set as GOVUK_NOTIFY_API_KEY"
        )
    response = self.api_client.send_email_notification(
        email_address=email_address,  # required string
        template_id=template_id,  # required UUID string
        personalisation=personalisation,  # optional dictionary
    )
    return response
