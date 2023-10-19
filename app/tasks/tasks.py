from celery import current_app as app
from models.email import Email
import logging
from app.notify import send_email

logger = logging.getLogger("uvicorn")


class EmailTask(app.Task):
    def handle_notify_exception(self, exception: Exception, email: Email):
        status_code = exception.status_code
        message = exception.message

        logger.error(f"Notify error: {status_code} - {message}")

        email.retry_count += 1
        raise self.retry(exc=exception, countdown=2**email.retry_count * 5, max_retries=10)


@app.task(bind=True, base=EmailTask)
def email_task(self, email: Email):
    try:
        send_email(email)
    except Exception as exception:
        self.handle_notify_exception(exception, email)
