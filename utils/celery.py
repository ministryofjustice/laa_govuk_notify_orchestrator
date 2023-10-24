from celery.result import AsyncResult
from config import Config


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    return result


def get_message_queue_protocol():
    if "amqp://" in Config.CELERY_BROKER_URL:
        return "AMQP"
    if "sqs://" in Config.CELERY_BROKER_URL:
        return "SQS"
