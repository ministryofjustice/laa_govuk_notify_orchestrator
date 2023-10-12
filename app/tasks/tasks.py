from celery import current_app as app
from models.email import Email
import logging

logger = logging.getLogger("uvicorn")


@app.task(name="email:email_task")
def email_task(email: Email, MessageGroupId="EmailQueue"):
    logger.info(f"Email object read from queue {email}")
