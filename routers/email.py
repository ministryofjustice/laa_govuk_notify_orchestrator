from config import Config
from fastapi.routing import APIRouter
from app.tasks.tasks import email_task
from models.request_models.email import Email as EmailRequest
from models.email import Email
from routers.docs.email_router import EmailRouter
from utils.deduplication import get_deduplication_id
from datetime import datetime
from kombu.exceptions import OperationalError


email_router = APIRouter()


@email_router.post("/email", summary=EmailRouter.summary, description=EmailRouter.description, status_code=201)
async def send_email(email_request: EmailRequest):
    """
    API Endpoint for email route.
    Recieves an email object and loads it onto the FIFO Queue.
    A 422 response is sent if the email_request object is found to be invalid by pydantic
    A 201 response is sent if the email_request object is valid

        Parameters:
            email_request (EmailRequest): An email object from the /email endpoint.
                                   Please see models/request_models/email for the definition
    """
    email = Email(email_request)

    # This is used as a factor in the deduplication_id to ensure that genuine duplicate emails are not removed as duplicates
    email.origin_time = datetime.now()

    message_properties = {
        "MessageGroupId": Config.MESSAGE_GROUP_ID,
        "MessageDeduplicationId": get_deduplication_id(email),
    }

    if Config.TESTING_MODE:
        # If we are running Unit Tests we do not want to place the email object on a message queue.
        return

    try:
        email_task.apply_async((email,), **message_properties)
    except OperationalError:
        raise OperationalError("Please ensure your Message Queue environment variables are set correctly.")
    return
