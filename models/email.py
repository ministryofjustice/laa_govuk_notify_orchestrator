from datetime import datetime
from models.request_models.email import Email as EmailRequest


class Email(EmailRequest):
    """
    This is the Email model, which defines what an email object on the message queue looks like.
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
