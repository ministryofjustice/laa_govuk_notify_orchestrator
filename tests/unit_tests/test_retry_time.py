from app.email import Email
from models.request_models.email import Email as EmailRequest
from tests.test_data.email import TestData


class TestRetryTime:
    def setup_method(self):
        email_request = EmailRequest.model_validate(TestData.valid_email_request)
        self.email = Email(email_request)

    def test_valid_count(self):
        expected_retry_time_seconds = [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 7200, 7200, 7200]

        for expected_result in expected_retry_time_seconds:
            self.email.retry_count += 1
            assert self.email.get_retry_time_seconds() == expected_result

    def test_invalid_count(self):
        self.email.retry_count = 0
        assert self.email.get_retry_time_seconds() == 300

    def test_invalid_data_type(self):
        self.email.retry_count = "apple"
        assert self.email.get_retry_time_seconds() == 300

    def test_no_retry_count(self):
        self.email.retry_count = None
        assert self.email.get_retry_time_seconds() == 300
