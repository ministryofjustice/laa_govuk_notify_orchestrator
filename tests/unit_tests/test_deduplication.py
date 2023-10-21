import pytest
from tests.test_data.deduplication import TestData
from utils.deduplication import get_deduplication_id


class Email:
    def __init__(self, email_address, template_id, personalisation):
        """
        This is used to model the Email object for unit testing utility functions which require an email object.
        Email objects are usually created by FastAPI using the /email endpoint.
        """
        self.email_address = email_address
        self.template_id = template_id
        self.personalisation = personalisation


class TestDeduplication:
    def test_valid_email_object(self):
        test_data = TestData.valid_email_request
        email = Email(test_data["email_address"], test_data["template_id"], test_data["personalisation"])
        email.origin_time = TestData.valid_email_request["origin_time"]
        assert get_deduplication_id(email) == "74b368e3dfc59f845a9d41098d0a300d1f65fa840957dfe184447d4c3543a4e1"

    def test_idential_email(self):
        test_data = TestData.identical_email_request
        email = Email(test_data["email_address"], test_data["template_id"], test_data["personalisation"])
        email.origin_time = TestData.valid_email_request["origin_time"]
        assert get_deduplication_id(email) == "74b368e3dfc59f845a9d41098d0a300d1f65fa840957dfe184447d4c3543a4e1"

    def test_valid_email_request_different_origin_time(self):
        test_data = TestData.valid_email_request_different_origin_time
        email = Email(test_data["email_address"], test_data["template_id"], test_data["personalisation"])
        email.origin_time = test_data["origin_time"]
        assert get_deduplication_id(email) == "8be6864d89638ab156bcd50bd959535bd0fb518987d0386d36308f13f5860480"

    def test_no_origin_time(self):
        test_data = TestData.no_origin_time
        email = Email(test_data["email_address"], test_data["template_id"], test_data["personalisation"])
        with pytest.raises(AttributeError) as excinfo:
            get_deduplication_id(email)
        assert str(excinfo.value) == "Missing required email field 'Email' object has no attribute 'origin_time'"
