from app.tasks.email import EmailTask
from notifications_python_client.errors import HTTPError, APIError, HTTP503Error, InvalidResponse, TokenError
from requests.models import Response


class TestLogErrorMessage:
    def test_token_error(self, caplog):
        error = TokenError(message="Token error message", token="Token")
        EmailTask.log_error_message(error)
        assert "CRITICAL" in caplog.text
        assert "Notify error: TokenError - Token error message. See our requirements for JSON Web Tokens" in caplog.text

    def test_http_error_4xx(self, caplog):
        response = Response()
        response.status_code = 403
        error = HTTPError(response=response, message="Internal server error")
        EmailTask.log_error_message(error)
        assert "CRITICAL" in caplog.text
        assert 'Notify error: 403 - Internal server error' in caplog.text

    def test_http_error_5xx(self, caplog):
        response = Response()
        response.status_code = 500
        error = HTTPError(response=response, message="Internal server error")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert 'Notify error: 500 - Internal server error' in caplog.text

    def test_http_503_error(self, caplog):
        response = Response()
        response.status_code = 503
        error = HTTP503Error(response=response, message="503 error message")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert "Notify error: 503 - 503 error message" in caplog.text

    def test_key_error(self, caplog):
        error = KeyError("Error message")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert "Notify error: KeyError - 'Error message'" in caplog.text

    def test_api_error(self, caplog):
        response = Response()
        error = APIError(response=response, message="API error message")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert "Notify error: APIError - None - API error message" in caplog.text

    def test_invalid_response(self, caplog):
        response = Response()
        error = InvalidResponse(response=response, message="Invalid response message")
        EmailTask.log_error_message(error)
        assert "ERROR" in caplog.text
        assert "Notify error: InvalidResponse - None - Invalid response message" in caplog.text
