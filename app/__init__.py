import logging
from app.main import create_app
from config import Config
import sentry_sdk

if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=0.1,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=0.1,
        environment=Config.ENVIRONMENT,
    )

logger = logging.getLogger("uvicorn")
notify_orchestrator_api = create_app()
celery = notify_orchestrator_api.celery_app
