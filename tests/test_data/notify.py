class TestData:
    valid_email_request = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "382cc41c-b81d-4197-8819-2ad76522d03d",
        "personalisation": {"full_name": "Test", "case_reference": "Reference"},
    }

    invalid_email_address = {
        "email_address": "This is not an email address",
        "template_id": "12345",
        "personalisation": {},
    }

    blank_email_address = {"email_address": "", "template_id": "12345", "personalisation": {}}

    no_email_address = {"email_address": None, "template_id": "12345", "personalisation": {}}

    no_template_id = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": None,
        "personalisation": {},
    }

    blank_template_id = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "",
        "personalisation": {},
    }

    no_personalisation = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "12345",
        "personalisation": None,
    }

    empty_personalisation = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "12345",
        "personalisation": {},
    }

    non_existant_personalisation = {
        "email_address": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "12345",
    }

    invalid_payload = {
        "incorrect_name": "simulate-delivered@notifications.service.gov.uk",
        "template_id": "12345",
        "personalisation": {},
    }

    empty_payload = {}

    no_payload = {}
