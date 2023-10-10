import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    # To change the host and port without altering the config files
    # use the --host & --port optional arguments when you run manage.py
    HOST = "127.0.0.1"
    PORT = 8026

    TITLE = "LAA GOV.UK Notify Orchestrator"

    SUMMARY = "API used for Email orchestration between CLA services and GOV.UK Notify."

    VERSION = "0.0.1"

    TERMS_OF_SERVICE = "https://github.com/ministryofjustice/.github/blob/main/CODE_OF_CONDUCT.md"

    CONTACT_INFO = {
        "name": "Legal Aid Agency",
        "url": "https://mojdigital.blog.gov.uk/",
        "email": "civil-legal-advice@digital.justice.gov.uk",
    }

    LICENCE_INFO = {
        "name": "MIT License",
        "url": "https://github.com/ministryofjustice/.github/blob/main/LICENSE"
    }

    TESTING_MODE = os.environ.get('TESTING_MODE') == 'True'
    
    try:
        QUEUE_NAME = os.environ['QUEUE_NAME']
    except KeyError:
        raise KeyError("QUEUE_NAME is a required environment variable")

    try:
        QUEUE_URL = os.environ['QUEUE_URL']
    except KeyError:
        raise KeyError("QUEUE_URL is a required environment variable")

    try:
        CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
    except KeyError:
        raise KeyError("CELERY_BROKER_URL is a required environment variable")
