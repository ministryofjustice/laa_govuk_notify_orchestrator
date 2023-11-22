from celery import current_app as app
from config import Config
from app.email import Email
import datetime as dt
from notifications_python_client.errors import HTTPError, TokenError
import logging

logger = logging.getLogger("uvicorn")


class EmailTask(app.Task):
    rate_limit_exceeded = False
    datetime_rate_limit_resets = None

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
        if isinstance(exception, TokenError):
            logger.critical(f"Notify error: {exception.__class__.__name__} - {exception.message}")
            return

        if not isinstance(exception, HTTPError):
            logger.error(f"Notify error: {exception.__class__.__name__} - {exception}")
            return

        log_method = logger.critical if exception.status_code in range(400, 499) else logger.error

        if isinstance(exception.message, str):
            log_method(f"Notify error: {exception.status_code} - {exception.message}")
            return

        for error in exception.message:
            try:
                message = f"{error['error']}: {error['message']}"
            except KeyError:
                message = f"{error}"
            log_method(f"Notify error: {exception.status_code} - {message}")

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

    @staticmethod
    def is_exception_http_429(exception: Exception) -> bool:
        if not isinstance(exception, HTTPError):
            return False
        try:
            return exception.status_code == 429
        except KeyError:
            return False
        return False

    @staticmethod
    def get_datetime_of_next_midnight():
        now = dt.datetime.now()
        midnight = dt.datetime.min.time()
        today_midnight = dt.datetime.combine(now, midnight)
        return today_midnight + dt.timedelta(days=1)


@app.task(bind=True, base=EmailTask)
def email_task(self, email: Email):
    try:
        if EmailTask.rate_limit_exceeded:
            if dt.now() > EmailTask.datetime_rate_limit_resets:
                EmailTask.rate_limit_exceeded = False
            else:
                raise RuntimeError(
                    "Rate limit has been exceeded, will not attempt to send any more emails until midnight."
                )
        email.send_email()
    except Exception as exception:
        if EmailTask.is_exception_http_429(exception):
            EmailTask.rate_limit_exceeded = True
            EmailTask.datetime_rate_limit_resets = EmailTask.get_datetime_of_next_midnight()
        self.log_error_message(exception)
        self.retry_email(email, exception)
