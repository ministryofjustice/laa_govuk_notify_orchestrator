from fastapi.testclient import TestClient
from app import app
from tests.utils.error_messages import ErrorMessages
from tests.test_data import TestData

TEST_SERVER_URL = "http://testserver"

test_client = TestClient(app)


class TestEmail:
    endpoint = "/email"

    def test_valid_email(self):

        res = test_client.post("/email", json=TestData.valid_email_request)

        assert res.status_code == 201, \
            ErrorMessages.invalid_status_code(201, res.status_code)

    def test_invalid_email(self):

        res = test_client.post("/email", json=TestData.invalid_email_request)

        assert res.status_code == 422, \
            ErrorMessages.invalid_status_code(422, res.status_code)
      
    def test_blank_email(self):
        res = test_client.post("/email", json=TestData.invalid_email_request)

        assert res.status_code == 422, \
            ErrorMessages.invalid_status_code(422, res.status_code)


class TestTemplateID:
    endpoint = "/email"

    def test_no_template_id(self):
        res = test_client.post("/email", json=TestData.no_template_id)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Input should be a valid string"

        assert res.status_code == 422, \
            ErrorMessages.invalid_status_code(422, res.status_code)

    def test_blank_template_id(self):
        res = test_client.post("/email", json=TestData.blank_template_id)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "String should have at least 1 characters"

        assert res.status_code == 422, \
            ErrorMessages.invalid_status_code(422, res.status_code)


class TestPersonalisation:
    endpoint = "/email"

    def test_no_personalisation(self):
        res = test_client.post("/email", json=TestData.no_personalisation)

        json_response = res.json()['detail'][0]

        assert json_response["msg"] == "Input should be a valid dictionary"

        assert res.status_code == 422, \
            ErrorMessages.invalid_status_code(422, res.status_code)

    def test_empty_personalisation(self):
        res = test_client.post("/email", json=TestData.empty_personalisation)

        assert res.status_code == 201, \
            ErrorMessages.invalid_status_code(201, res.status_code)
