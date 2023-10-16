from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse


root_router = APIRouter()


@root_router.get("/", response_class=RedirectResponse, include_in_schema=False)
def read_root():
    """
    API Endpoint for "/".
    Automatically redirects the user to the documentation if attempting to view the root of the service.
    """
    return RedirectResponse(url="/redoc")
