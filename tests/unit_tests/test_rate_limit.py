from app.tasks.email import EmailTask


class TestSetRateLimitExceeded:
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
