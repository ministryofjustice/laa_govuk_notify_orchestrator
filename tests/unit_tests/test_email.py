from fastapi.testclient import TestClient
from app import notify_orchestrator_api as app
from tests.utils.error_messages import ErrorMessages
from tests.test_data.email import TestData

TEST_SERVER_URL = "http://testserver"

test_client = TestClient(app)


class TestEmail:
    endpoint = "/email"

    def test_valid_email(self):
        res = test_client.post("/email", json=TestData.valid_email_request)

        assert res.status_code == 201, ErrorMessages.invalid_status_code(201, res.status_code)

    def test_invalid_email(self):
        res = test_client.post("/email", json=TestData.invalid_email_address)

        json_response = res.json()["detail"][0]

        assert "value is not a valid email address" in json_response["msg"]

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_blank_email(self):
        res = test_client.post("/email", json=TestData.blank_email_address)

        json_response = res.json()["detail"][0]

        assert "value is not a valid email address" in json_response["msg"]

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_no_email(self):
        res = test_client.post("/email", json=TestData.no_email_address)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Input should be a valid string"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)


class TestTemplateID:
    endpoint = "/email"

    def test_no_template_id(self):
        res = test_client.post("/email", json=TestData.no_template_id)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Input should be a valid string"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_blank_template_id(self):
        res = test_client.post("/email", json=TestData.blank_template_id)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "String should have at least 1 characters"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)


class TestPersonalisation:
    endpoint = "/email"

    def test_no_personalisation(self):
        res = test_client.post("/email", json=TestData.no_personalisation)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Input should be a valid dictionary"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_empty_personalisation(self):
        res = test_client.post("/email", json=TestData.empty_personalisation)

        assert res.status_code == 201, ErrorMessages.invalid_status_code(201, res.status_code)

    def test_non_existant_personalisation(self):
        res = test_client.post("/email", json=TestData.non_existant_personalisation)

        assert res.status_code == 201, ErrorMessages.invalid_status_code(201, res.status_code)


class TestPayload:
    endpoint = "/email"

    def test_invalid_payload(self):
        res = test_client.post("/email", json=TestData.invalid_payload)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Field required"

        assert json_response["loc"][1] == "email_address"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_empty_payload(self):
        res = test_client.post("/email", json=TestData.empty_payload)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Field required"

        assert json_response["loc"][1] == "email_address"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)

    def test_no_payload(self):
        res = test_client.post("/email", json=TestData.no_payload)

        json_response = res.json()["detail"][0]

        assert json_response["msg"] == "Field required"

        assert json_response["loc"][1] == "email_address"

        assert res.status_code == 422, ErrorMessages.invalid_status_code(422, res.status_code)


class TestInvalidMethod:
    def test_get(self):
        res = test_client.get("/email")

        assert res.status_code == 405, ErrorMessages.invalid_status_code(405, res.status_code)

    def test_put(self):
        res = test_client.put("/email", json=TestData.valid_email_request)

        assert res.status_code == 405, ErrorMessages.invalid_status_code(405, res.status_code)
