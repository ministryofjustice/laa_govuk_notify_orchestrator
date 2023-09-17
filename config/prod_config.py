import os


class ProductionConfig:
    SECRET_KEY = os.eniron.get("SECRET_KEY", "None")
