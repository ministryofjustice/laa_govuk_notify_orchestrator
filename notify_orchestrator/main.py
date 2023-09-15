from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import logging
from notify_orchestrator import config

app = FastAPI(
    title=config.TITLE,
    summary=config.SUMMARY,
    version=config.VERSION,
    terms_of_service=config.TERMS_OF_SERVICE,
    license_info=config.LICENCE_INFO,
)

logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")


@app.get("/", response_class=RedirectResponse)
def read_root():
    return RedirectResponse(url='/redoc')
