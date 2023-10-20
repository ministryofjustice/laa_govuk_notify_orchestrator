from unittest.mock import patch

from models.email import Email
from models.request_models.email import Email as EmailRequest
from app.tasks.email import email_task

from tests.test_data.notify import TestData

from notifications_python_client.errors import HTTPError


class TestSendEmail:
    @patch("models.email.Email.send_email")
    def test_success(self, send_email):
        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        email = Email(email_request)
        email_task(email)
        send_email.assert_called()

    @patch("models.email.Email.send_email")
    @patch("app.tasks.email.EmailTask.retry_email")
    def test_failure(self, send_email, retry_email):
        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        email = Email(email_request)
        send_email.side_effect = HTTPError()

        email_task(email)
        retry_email.assert_called()
