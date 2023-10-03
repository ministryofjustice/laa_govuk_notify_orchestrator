from app import notify_orchestrator_api
from app import logger


@notify_orchestrator_api.on_event("startup")
def on_startup():
    logger.info(f"Documentation can be found at the {notify_orchestrator_api.docs_url} "
                f"or {notify_orchestrator_api.redoc_url} endpoints.")
