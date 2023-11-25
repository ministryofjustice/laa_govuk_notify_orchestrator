from celery import current_app as app
from config import Config
from app.email import Email
from notifications_python_client.errors import HTTPError, TokenError, APIError
import datetime as dt
import logging

logger = logging.getLogger("uvicorn")


class EmailTask(app.Task):
    # This is set to None if the rate limit has not been exceeded, it will be set to the next rate limit reset time if it has previously been exceeded.
    _datetime_rate_limit_resets = None

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

    @property
    def rate_limit_exceeded(self) -> bool:
        """
        This is a getter to check if the rate limit has been exceeded.
        If the rate limit was exceeded on a previous day then it will return False.
        """
        if EmailTask._datetime_rate_limit_resets is None:
            return False
        if dt.datetime.now() > EmailTask._datetime_rate_limit_resets:
            self.rate_limit_exceeded = False
            return False
        return True

    @rate_limit_exceeded.setter
    def rate_limit_exceeded(self, value: bool):
        """
        If the rate limit has deemed to be exceeded _datetime_rate_limit_resets will be set to the next rate limit reset time.
        Else will be set to None, indicating the rate limit has not been reached.
        """
        EmailTask._datetime_rate_limit_resets = EmailTask.get_datetime_of_next_rate_limit_reset() if value else None

    @staticmethod
    def is_rate_limit_exception(exception: Exception) -> bool:
        """
        This returns True if the exception raised is due to hitting the API Rate Limit.
        GOV.UK Notify specify that an HTTP 429 will be raised if this rate limit is reached.
        """
        RATE_LIMIT_ERROR_CODES = [429]
        if not isinstance(exception, HTTPError):
            return False
        try:
            return exception.status_code in RATE_LIMIT_ERROR_CODES
        except AttributeError:
            return False

    @staticmethod
    def get_datetime_of_next_rate_limit_reset():
        """
        GOV.UK Notify's rate limiter resets at midnight, this will get the datetime of the next reset.
        """
        today = dt.datetime.now().date()
        midnight = dt.datetime.min.time()
        today_midnight = dt.datetime.combine(date=today, time=midnight)
        return today_midnight + dt.timedelta(days=1)


@app.task(bind=True, base=EmailTask)
def email_task(self, email: Email):
    """
    This is the task associated with an email request.
    It will attempt to send an email to GOV.UK Notify if the rate limit  has not been exceeded.
    If an error is raised from Notify it will be logged and the task re-queued using an exponential back-off.

        Parameters:
            email (Email): An email object, generated by the /email endpoint.
    """
    try:
        if self.rate_limit_exceeded:
            raise APIError(
                "GOV.UK Notify's rate limit has been exceeded, will not attempt to send any more emails until midnight."
            )
        email.send_email()
    except Exception as exception:
        if EmailTask.is_rate_limit_exception(exception):
            self.rate_limit_exceeded = True
        self.log_error_message(exception)
        self.retry_email(email, exception)
