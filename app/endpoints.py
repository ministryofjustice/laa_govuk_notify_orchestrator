from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/", response_class=RedirectResponse)
def read_root():
    return RedirectResponse(url='/redoc')
