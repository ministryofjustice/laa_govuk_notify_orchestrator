from fastapi.routing import APIRouter
from models.request_models.email import Email
from app.tasks.tasks import email_task
from routers.docs.email_router import EmailRouter


email_router = APIRouter()


@email_router.post("/email", summary=EmailRouter.summary, description=EmailRouter.description, status_code=201)
async def send_email(email_request: Email):
    """
    API Endpoint for email route.
    Recieves an email object and loads it onto the FIFO Queue.
    A 422 response is sent if the email_request object is found to be invalid by pydantic
    A 201 response is sent if the email_request object is valid

        Parameters:
            email_request (Email): An email object from the /email endpoint.
                                   Please see models/request_models/email for the definition
    """
    email_task.apply_async((email_request,))
    return
