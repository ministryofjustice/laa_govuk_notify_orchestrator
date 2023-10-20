from celery import current_app as app
from config import Config
from models.email import Email
from notifications_python_client.errors import HTTPError
import logging

logger = logging.getLogger("uvicorn")


class EmailTask(app.Task):
    def retry_email(self, email: Email, exception: Exception):
        """
        This increments the retry_count and calls a retry on the task with the exception that caused the retry passed in.
        If after the maximum number of retries the task still fails then the exception will be raised and the email will be lost.
        With 32 retries the email will only be lost if we are unable to get a response after ~24 hours.
        """
        email.retry_count += 1
        raise self.retry(exc=exception, countdown=email.get_retry_time_seconds(), max_retries=Config.MAX_RETRIES)

    @staticmethod
    def log_error_message(exception: Exception):
        if not isinstance(exception, HTTPError):
            logger.error(exception)
            return

        for error_message in exception.message:
            try:
                logger.error(
                    f"Notify error: {exception.status_code} - {error_message['error']}: {error_message['message']}"
                )
            except KeyError:
                logger.error(f"Notify error: {exception.status_code} - {error_message.message}")


@app.task(bind=True, base=EmailTask)
def email_task(self, email: Email):
    try:
        email.send_email()
    except Exception as exception:
        self.log_error_message(exception)
        self.retry_email(email, exception)
