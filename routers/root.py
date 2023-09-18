from routers import router
from fastapi.responses import RedirectResponse


@router.get("/", response_class=RedirectResponse)
def read_root():
    return RedirectResponse(url='/redoc')
