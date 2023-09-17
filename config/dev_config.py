import os


class DevConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "None")
