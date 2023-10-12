import hashlib
from models.request_models.email import Email


def get_deduplication_id(email: Email) -> str:
    """
    Utility function to get the deduplication_id for an email object.
    The factors used to determine the deduplication factor are:
        - Email Address
        - Template ID
        - Personalisation Dict
        - Email origin time (Set once, when the email arrives at the endpoint)

        Parameters:
            email (Email): An email object from the /email endpoint.
                            Please see models/request_models/email for the definition
    """

    sha = hashlib.sha256()

    try:
        email_deduplication_fields = f"{email.email_address}{email.template_id}{email.personalisation}{email.origin_time}"
    except AttributeError as e:
        raise AttributeError(f"Missing required email field {e}")

    sha.update(email_deduplication_fields.encode())
    return sha.hexdigest()
