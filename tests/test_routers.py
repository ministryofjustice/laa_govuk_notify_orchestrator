from fastapi.testclient import TestClient
from app import notify_orchestrator_api as app
from tests.utils.error_messages import ErrorMessages

TEST_SERVER_URL = "http://testserver"

test_client = TestClient(app)


class TestRedirection:
    endpoint = "/"

    def test_root_redirection(self):

        res = test_client.get(self.endpoint)

        assert res.url == f"{TEST_SERVER_URL}/redoc", \
            ErrorMessages.invalid_url(f"{TEST_SERVER_URL}/redoc", res.url)

        assert res.status_code == 200, \
            ErrorMessages.invalid_status_code(200, res.status_code)

    def test_root_redirection_disallow_redirect(self):

        res = test_client.get(self.endpoint, follow_redirects=False)

        assert res.url == f"{TEST_SERVER_URL}/", \
            ErrorMessages.invalid_url(f"{TEST_SERVER_URL}/", res.url)

        assert res.status_code == 307, \
            ErrorMessages.invalid_status_code(307, res.status_code)
