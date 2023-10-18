from config import Config
from celery import current_app as celery_app
import boto3


def is_queue_alive() -> bool:
    """
    Returns True if the active queue, as determined by Config.QUEUE_NAME is alive.

    If you are using AMQP as the Message Broker protocol then it will ping the celery workers

    If you are using SQS as the Message Broker protocol then it will find the URL of the queue with the given Config QUEUE_NAME and ensure that the QUEUE_URL matches,
    if this matches then the queue can be found and the client must have the required permissions.
    We use this method because SQS does not yet support worker remote control commands. https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/sqs.html
    """
    if "amqp://" in Config.CELERY_BROKER_URL:
        inspector = celery_app.control.inspect()
        worker_response = inspector.active_queues()
        if len(worker_response) == 0:
            return False
        for worker in worker_response:
            queues = worker_response[worker]
            if len(queues) == 0:
                return False
            for queue in queues:
                try:
                    if queue["name"] == Config.QUEUE_NAME:
                        return True
                except KeyError:
                    return False
        return False

    if "sqs://" in Config.CELERY_BROKER_URL:
        client = boto3.client("sqs")
        return client.get_queue_url(QueueName=Config.QUEUE_NAME) == Config.QUEUE_URL

    return False
