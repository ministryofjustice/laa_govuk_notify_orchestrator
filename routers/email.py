from fastapi.routing import APIRouter
from models.request_models.email import Email
from fastapi import BackgroundTasks
from app.add_email import add_email_to_queue


email_router = APIRouter()


@email_router.post("/email", summary="Send email to GOV.UK Notify", description="Will queue your email to be sent to GOV.UK Notify,\
                    if their service is down the email will be held in an encrypted queue until a response is recieved.\
                    If after two weeks no response is recieved your email be deleted.", status_code=201)
async def send_email(email_request: Email, background_tasks: BackgroundTasks):
    background_tasks.add_task(add_email_to_queue, email_request)
    return
