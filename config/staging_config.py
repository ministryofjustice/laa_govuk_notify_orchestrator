import os


class StagingConfig:
    SECRET_KEY = os.eniron.get("SECRET_KEY", None)
