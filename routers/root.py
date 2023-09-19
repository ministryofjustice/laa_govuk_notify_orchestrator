from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse


root_router = APIRouter()


@root_router.get("/", response_class=RedirectResponse, include_in_schema=False)
def read_root():
    return RedirectResponse(url='/redoc')
