from fastapi.routing import APIRouter
from utils.status import is_queue_alive
from fastapi import HTTPException


status_router = APIRouter()


@status_router.get("/status")
def read_status():
    """
    API Endpoint for "/status".
    Returns 200 if the service is alive.
    """
    if not is_queue_alive():
        raise HTTPException(status_code=503, detail="Queue could not be found")
    return {"status": "ok"}
