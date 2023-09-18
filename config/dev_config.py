from config.base_config import BaseConfig
import os


class DevConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "None")
    TITLE = "LAA GOV.UK Notify Orchestrator [Development]"
