from fastapi.routing import APIRouter
from config import Config
from celery import current_app as celery_app
import boto3


status_router = APIRouter()


@status_router.get("/status")
def read_status():
    """
    API Endpoint for "/status".
    Returns 200 if the service is alive.
    """
    if "amqp://" in Config.CELERY_BROKER_URL:
        inspector = celery_app.control.inspect()
        is_celery_worker_alive = inspector.ping()
        response = {"status": is_celery_worker_alive}
        return response
    if "sqs://" in Config.CELERY_BROKER_URL:
        client = boto3.client("sqs")
        response = {"status": client.get_queue_url(QueueName=Config.QUEUE_NAME)}
        return response
