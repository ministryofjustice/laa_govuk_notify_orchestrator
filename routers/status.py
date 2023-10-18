from fastapi.routing import APIRouter


status_router = APIRouter()


@status_router.get("/status")
def read_status():
    """
    API Endpoint for "/status".
    Returns 200 if the service is alive.
    """
    response = {"status": "ok"}
    return response
