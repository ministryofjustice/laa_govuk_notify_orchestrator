from fastapi import FastAPI
from notify_orchestrator import config
from notify_orchestrator.endpoints import router
import logging


app = FastAPI(
    title=config.TITLE,
    summary=config.SUMMARY,
    version=config.VERSION,
    terms_of_service=config.TERMS_OF_SERVICE,
    license_info=config.LICENCE_INFO,
)

app.include_router(router)

logger = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup_event():
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")
