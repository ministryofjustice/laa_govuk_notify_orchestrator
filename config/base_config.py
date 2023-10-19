import os
from dotenv import load_dotenv


load_dotenv()

environment_exception_message = (
    "is a required environment variable. " "You can set up a valid .env file by running:\n" "cp .env.example .env"
)


class BaseConfig:
    # To change the host and port without altering the config files
    # use the --host & --port optional arguments when you run manage.py
    HOST = "127.0.0.1"
    PORT = 8026

    # Used to populate the OpenAPI Documentation
    TITLE = "LAA GOV.UK Notify Orchestrator"

    SUMMARY = "API used for Email orchestration between CLA services and GOV.UK Notify."

    VERSION = "0.0.1"

    TERMS_OF_SERVICE = "https://github.com/ministryofjustice/.github/blob/main/CODE_OF_CONDUCT.md"

    CONTACT_INFO = {
        "name": "Legal Aid Agency",
        "url": "https://mojdigital.blog.gov.uk/",
        "email": "civil-legal-advice@digital.justice.gov.uk",
    }

    LICENCE_INFO = {"name": "MIT License", "url": "https://github.com/ministryofjustice/.github/blob/main/LICENSE"}

    # Used for AWS SQS, every message must have a group
    MESSAGE_GROUP_ID = "EmailQueue"

    # If testing mode is enabled then the endpoint will not attempt to place the email on the queue
    TESTING_MODE = os.environ.get("TESTING_MODE") == "True"

    try:
        QUEUE_NAME = os.environ["QUEUE_NAME"]
    except KeyError as e:
        if not TESTING_MODE:
            raise EnvironmentError(f"{e}{environment_exception_message}")
        QUEUE_NAME = ""

    try:
        QUEUE_URL = os.environ["QUEUE_URL"]
    except KeyError as e:
        if not TESTING_MODE:
            raise EnvironmentError(f"{e}{environment_exception_message}")
        QUEUE_URL = ""

    try:
        # If this starts with AMPQ celery will attempt to use the Advanced Message Queue Protocol
        # If this starts with SQS celery will attempt to use the Simple Queuing Service Protocol
        CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
    except KeyError as e:
        if not TESTING_MODE:
            raise EnvironmentError(f"{e}{environment_exception_message}")
        CELERY_BROKER_URL = ""

    try:
        GOVUK_NOTIFY_API_KEY = os.environ["GOVUK_NOTIFY_API_KEY"]
    except KeyError as e:
        if not TESTING_MODE:
            raise EnvironmentError(f"{e}{environment_exception_message}")
        GOVUK_NOTIFY_API_KEY = ""
