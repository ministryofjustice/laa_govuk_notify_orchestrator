import logging
from app.main import app

notify_orchestrator_api = app
celery = app.celery_app
logger = logging.getLogger("uvicorn")
