from app.tasks.email import EmailTask
from notifications_python_client.errors import HTTPError
from requests.models import Response


class TestLogErrorMessage:
    def test_http_error_5xx(self, caplog):
        response = Response()
        response.status_code = 500
        error = HTTPError(response=response, message="Internal server error")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert 'Notify error: 500 - Internal server error' in caplog.text

    def test_http_error_4xx(self, caplog):
        response = Response()
        response.status_code = 403
        error = HTTPError(response=response, message="Internal server error")
        EmailTask.log_error_message(error)
        assert "CRITICAL" in caplog.text
        assert 'Notify error: 403 - Internal server error' in caplog.text

    def test_key_error(self, caplog):
        error = KeyError("Error message")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert "Notify error: KeyError - 'Error message'" in caplog.text
