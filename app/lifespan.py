import logging
from contextlib import asynccontextmanager
from config import Config

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app):
    on_startup(app)
    yield
    on_shutdown(app)


def on_startup(app):
    logger.info(f"Documentation can be found at the {app.docs_url} " f"or {app.redoc_url} endpoints.")
    logger.info("Using the following queue configuation:")
    logger.info(f"Queue name: {Config.QUEUE_NAME}")
    logger.info(f"Queue URL: {Config.QUEUE_URL}")


def on_shutdown(app):
    logger.info(f"{app.title} has shutdown")
