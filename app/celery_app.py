from config import Config
from celery import current_app as current_celery_app


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(Config, namespace="CELERY")
    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer="pickle")
    celery_app.conf.update(result_serializer="pickle")
    celery_app.conf.update(accept_content=["pickle", "json"])
    celery_app.conf.update(result_persistent=True)
    celery_app.conf.update(worker_send_task_events=False)
    celery_app.conf.update(worker_prefetch_multiplier=1)
    celery_app.conf.update(task_default_queue=Config.QUEUE_NAME)
    celery_app.conf.update(
        broker_transport_options={"predefined_queues": {Config.QUEUE_NAME: {"url": Config.QUEUE_URL}}}
    )

    return celery_app
