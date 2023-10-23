from datetime import datetime
from models.request_models.email import Email as EmailRequest
from app.notify import NotifyClient
from config import Config


class Email(EmailRequest):
    """
    This is the Email model, which defines what an email object on the message queue looks like.
    It is initalised based upon an EmailReqest, which defines the structure of an incoming payload.
    """

    origin_time: datetime = None
    retry_count: int = 0

    def __init__(self, email_request: EmailRequest):
        if not email_request.personalisation:
            email_request.personalisation = {}

        super().__init__(
            email_address=email_request.email_address,
            template_id=email_request.template_id,
            personalisation=email_request.personalisation,
        )

    def send_email(self):
        NotifyClient().send_email(self.email_address, self.template_id, self.personalisation)

    def get_retry_time_seconds(self) -> int:
        """
        Gets the time we should wait for before attempting to re-try sending the email to Notify.
        This is based on the retry_count of the email and increases exponentially up to a cap of every two hours.
        """
        if self.retry_count not in range(1, Config.MAX_RETRIES):
            # This should never be reached, however, if retry_count is not an expected value
            # we return 300, which causes retry the email again in 5 minutes.
            return 300

        MAX_RETRY_TIME_SECONDS = 2 * 60 * 60

        retry_time = 5 * (2**self.retry_count)  # 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120

        return retry_time if retry_time < MAX_RETRY_TIME_SECONDS else MAX_RETRY_TIME_SECONDS
