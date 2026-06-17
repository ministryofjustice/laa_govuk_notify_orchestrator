from unittest.mock import patch, MagicMock

from app.email import Email
from models.request_models.email import Email as EmailRequest
from app.tasks.email import email_task

from tests.test_data.notify import TestData

from notifications_python_client.errors import HTTPError


class TestSendEmail:
    @patch("app.email.Email.send_email")
    def test_success(self, send_email):
        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        email = Email(email_request)
        email_task(email)
        send_email.assert_called()

    @patch("app.email.Email.send_email")
    @patch("app.tasks.email.EmailTask.retry_email")
    def test_failure(self, send_email, retry_email):
        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        email = Email(email_request)
        send_email.side_effect = HTTPError()

        email_task(email)
        retry_email.assert_called()

    @patch("app.email.Email.send_email")
    @patch("app.tasks.email.EmailTask.retry_email")
    @patch("app.tasks.email.EmailTask.log_error_message")
    def test_400_response(self, log_error_message, retry_email, send_email):
        """Do not retry email after receiving 400 error from notification API"""

        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        email = Email(email_request)
        http_error = HTTPError()
        http_error.error = MagicMock(status_code=400)
        send_email.side_effect = http_error
        email_task(email)

        retry_email.assert_not_called()
        log_error_message.assert_not_called()
