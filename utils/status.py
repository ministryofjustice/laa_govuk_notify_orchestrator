from config import Config
from celery import current_app as celery_app
from utils.celery import get_message_queue_protocol
from botocore.exceptions import ClientError
import boto3


def is_queue_alive() -> bool:
    """
    Returns True if the active queue, as determined by Config.QUEUE_NAME is alive.

    If you are using AMQP as the Message Broker protocol then it will check that the queue name defined by Config.QUEUE_NAME has been created.

    If you are using SQS as the Message Broker protocol then it will find the URL of the queue with the given Config QUEUE_NAME and ensure that the QUEUE_URL matches,
    if this matches then the queue can be found and the client must have the required permissions.
    We use this method because SQS does not yet support worker remote control commands. https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/sqs.html
    """
    message_queue_protocol = get_message_queue_protocol()

    if message_queue_protocol == "AMQP":
        return is_rabbit_mq_queue_created(Config.QUEUE_NAME)

    if message_queue_protocol == "SQS":
        return is_sqs_queue_created(Config.QUEUE_NAME)

    return False


def is_rabbit_mq_queue_created(queue_name: str):
    """
    Returns True if there is a RabbitMQ Queue with the name specified in Config.QUEUE_NAME
    """
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
                if queue["name"] == queue_name:
                    return True
            except KeyError:
                return False
    return False


def is_sqs_queue_created(queue_name: str):
    """
    Returns True if the SQS Queue URL matches the Queue URL found when querying SQS.
    If this check passes then we know we have permission to query and interact with the queue
    and the resource has been created sucessfully.
    """
    client = boto3.client("sqs")
    try:
        response = client.get_queue_url(QueueName=queue_name)
    except ClientError:
        # If a client error is raised then the queue does not exists.
        return False
    try:
        return response["QueueUrl"] == Config.QUEUE_URL
    except KeyError:
        return False
