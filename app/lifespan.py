import logging
from contextlib import asynccontextmanager

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app):
    on_startup(app)
    yield
    on_shutdown(app)


def on_startup(app):
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")


def on_shutdown(app):
    logger.info(f"{app.title} has shutdown")

