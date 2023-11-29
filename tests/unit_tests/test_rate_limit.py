from app.tasks.email import EmailTask
from datetime import datetime
from freezegun import freeze_time
from notifications_python_client.errors import HTTPError, HTTP503Error, APIError
from requests.models import Response


class TestSetRateLimitExceeded:
    def test_default_value(self):
        email_task = EmailTask()
        assert email_task.rate_limit_exceeded is False

    def test_set_rate_limit(self):
        # This tests that the 'rate_limit_exceeded' attribute is correctly shared across all instances of EmailTask
        email_task_1 = EmailTask()
        email_task_2 = EmailTask()

        email_task_1.rate_limit_exceeded = True
        assert email_task_2.rate_limit_exceeded is True

    def test_rate_limit_reset_date_set(self):
        email_task = EmailTask()
        email_task.rate_limit_exceeded = True

        assert email_task._datetime_rate_limit_resets is not None
        assert email_task._datetime_rate_limit_resets == email_task.get_datetime_of_next_rate_limit_reset()

    def test_setting_rate_limit_exceeded_false_removes_datetime(self):
        email_task_1 = EmailTask()
        email_task_2 = EmailTask()

        email_task_1.rate_limit_exceeded = True

        assert email_task_2._datetime_rate_limit_resets is not None
        assert email_task_1._datetime_rate_limit_resets == email_task_1._datetime_rate_limit_resets

        email_task_2.rate_limit_exceeded = False
        assert email_task_1._datetime_rate_limit_resets is None
        assert email_task_2._datetime_rate_limit_resets is None

    def test_automatic_reset_of_rate_limit_exceeded(self):
        email_task = EmailTask()
        with freeze_time("2023-11-24 11:50:00"):
            email_task.rate_limit_exceeded = True
            assert email_task._datetime_rate_limit_resets == datetime(2023, 11, 25, 0, 0, 0)

        with freeze_time("2023-11-24 11:59:59"):
            assert email_task.rate_limit_exceeded is True

        with freeze_time("2023-11-25 0:0:0"):
            assert email_task.rate_limit_exceeded is True

        with freeze_time("2023-11-25 0:0:1"):
            assert email_task.rate_limit_exceeded is False


class TestGetDatetimeOfNextRateLimitReset:
    def test_random_tuesday(self):
        with freeze_time("2023-11-28 11:50:00"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2023, 11, 29, 0, 0, 0)

    def test_new_year(self):
        with freeze_time("2023-12-31 3:14:15"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2024, 1, 1, 0, 0, 0)

    def test_millennium_bug(self):
        with freeze_time("1999-12-31 3:14:15"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2000, 1, 1, 0, 0, 0)

    def test_at_midnight(self):
        with freeze_time("2025-01-01 0:0:0"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2025, 1, 2, 0, 0, 0)

    def test_daylight_saving_time(self):
        with freeze_time("2023-03-27 12:59:0"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2023, 3, 28, 0, 0, 0)

        with freeze_time("2023-03-27 1:0:0"):
            assert EmailTask.get_datetime_of_next_rate_limit_reset() == datetime(2023, 3, 28, 0, 0, 0)


class TestIsRateLimitException:
    def test_HTTP_429(self):
        response = Response()
        response.status_code = 429
        exception = HTTPError(response)
        assert EmailTask.is_rate_limit_exception(exception) is True

    def test_HTTP_500(self):
        response = Response()
        response.status_code = 500
        exception = HTTPError(response)
        assert EmailTask.is_rate_limit_exception(exception) is False

    def test_HTTP_403(self):
        response = Response()
        response.status_code = 403
        exception = HTTPError(response)
        assert EmailTask.is_rate_limit_exception(exception) is False

    def test_HTTP_503(self):
        response = Response()
        response.status_code = 403
        exception = HTTP503Error(response)
        assert EmailTask.is_rate_limit_exception(exception) is False

    def test_api_error(self):
        exception = APIError("Text")
        assert EmailTask.is_rate_limit_exception(exception) is False

    def test_key_error(self):
        exception = KeyError("Text")
        assert EmailTask.is_rate_limit_exception(exception) is False
