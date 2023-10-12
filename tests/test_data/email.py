class TestData:
    valid_email_request = {"email_address": "test@example.com", "template_id": "12345", "personalisation": {}}

    invalid_email_address = {
        "email_address": "This is not an email address",
        "template_id": "12345",
        "personalisation": {},
    }

    blank_email_address = {"email_address": "", "template_id": "12345", "personalisation": {}}

    no_email_address = {"email_address": None, "template_id": "12345", "personalisation": {}}

    no_template_id = {"email_address": "test@example.com", "template_id": None, "personalisation": {}}

    blank_template_id = {"email_address": "test@example.com", "template_id": "", "personalisation": {}}

    no_personalisation = {"email_address": "test@example.com", "template_id": "12345", "personalisation": None}

    empty_personalisation = {"email_address": "test@example.com", "template_id": "12345", "personalisation": {}}

    non_existant_personalisation = {
        "email_address": "test@example.com",
        "template_id": "12345",
    }

    invalid_payload = {"incorrect_name": "test@example.com", "template_id": "12345", "personalisation": {}}

    empty_payload = {}

    no_payload = {}
