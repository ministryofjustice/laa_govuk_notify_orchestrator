import logging
from app.main import create_app

notify_orchestrator_api = create_app()
celery = notify_orchestrator_api.celery_app
logger = logging.getLogger("uvicorn")
