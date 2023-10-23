from notifications_python_client.notifications import NotificationsAPIClient
from config import Config
import logging


logger = logging.getLogger("uvicorn")


class NotifyClient:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(NotifyClient, self).__new__(self)
            self.notify_client = NotificationsAPIClient(Config.GOVUK_NOTIFY_API_KEY)
        return self._instance

    def send_email(self, email_address: str, template_id: str, personalisation: dict):
        response = self.notify_client.send_email_notification(
            email_address=email_address,  # required string
            template_id=template_id,  # required UUID string
            personalisation=personalisation,  # optional dictionary
        )
        return response
