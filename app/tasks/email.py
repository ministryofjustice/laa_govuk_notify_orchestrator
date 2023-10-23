from celery import current_app as app
from config import Config
from app.email import Email
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
        raise self.retry(exc=exception, countdown=self.get_retry_time_seconds(email), max_retries=Config.MAX_RETRIES)

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

    @staticmethod
    def get_retry_time_seconds(email: Email) -> int:
        """
        Gets the time we should wait for before attempting to re-try sending the email to Notify.
        This is based on the retry_count of the email and increases exponentially up to a cap of every two hours.
        """
        if email.retry_count not in range(1, Config.MAX_RETRIES):
            # This should never be reached, however, if retry_count is not an expected value
            # we return 300, which causes retry the email again in 5 minutes.
            return 300

        MAX_RETRY_TIME_SECONDS = 7200  # 2 Hours

        retry_time = 5 * (2**email.retry_count)  # 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120

        return retry_time if retry_time < MAX_RETRY_TIME_SECONDS else MAX_RETRY_TIME_SECONDS


@app.task(bind=True, base=EmailTask)
def email_task(self, email: Email):
    try:
        email.send_email()
    except Exception as exception:
        self.log_error_message(exception)
        self.retry_email(email, exception)
