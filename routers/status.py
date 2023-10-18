from fastapi.routing import APIRouter
from celery import current_app as celery_app


status_router = APIRouter()


@status_router.get("/status")
def read_status():
    """
    API Endpoint for "/status".
    Returns 200 if the service is alive.
    """
    return celery_app.control.inspect().active()
