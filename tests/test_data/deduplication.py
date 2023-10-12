from datetime import datetime


class TestData:
    valid_email_request = {
        "email_address": "test@example.com",
        "template_id": "12345",
        "personalisation": {},
        "origin_time": datetime.fromisoformat('2023-11-04T00:05:23')
    }

    identical_email_request = {
        "email_address": "test@example.com",
        "template_id": "12345",
        "personalisation": {},
        "origin_time": datetime.fromisoformat('2023-11-04T00:05:23')
    }

    valid_email_request_different_origin_time = {
        "email_address": "test@example.com",
        "template_id": "12345",
        "personalisation": {},
        "origin_time": datetime.fromisoformat('2023-11-04T00:05:25')
    }

    no_origin_time = {
        "email_address": "test@example.com",
        "template_id": "12345",
        "personalisation": {},
    }
