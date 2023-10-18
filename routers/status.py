from fastapi.routing import APIRouter
from utils.celery import get_celery_status
from celery import current_app as celery_app


status_router = APIRouter()


@status_router.get("/status")
def read_status():
    """
    API Endpoint for "/status".
    Returns the celery worker status including the active queue
    """
    return get_celery_status(celery_app)
