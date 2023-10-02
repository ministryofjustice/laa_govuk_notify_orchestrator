from fastapi import FastAPI
from config import Config
from routers import routers
from config.celery_utils import create_celery
import logging

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=Config.TITLE,
    summary=Config.SUMMARY,
    version=Config.VERSION,
    terms_of_service=Config.TERMS_OF_SERVICE,
    license_info=Config.LICENCE_INFO,
)

app.celery_app = create_celery()

for router in routers:
    app.include_router(router)


@app.on_event("startup")
def on_startup():
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")
