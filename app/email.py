from datetime import datetime
from models.request_models.email import Email as EmailRequest
from app.notify import NotifyClient


class Email(EmailRequest):
    """
    This is the Email model, which defines what an email object on the message queue looks like.
    It is initialised based upon an EmailRequest, which defines the structure of an incoming payload.
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
        return NotifyClient().send_email(self.email_address, self.template_id, self.personalisation)
