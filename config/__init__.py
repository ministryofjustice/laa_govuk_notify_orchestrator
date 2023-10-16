import os
from .dev_config import DevConfig
from .staging_config import StagingConfig
from .prod_config import ProductionConfig

current_environment = os.environ.get("ENV", "development")

Config = (
    ProductionConfig
    if current_environment == "production"
    else StagingConfig
    if current_environment == "staging"
    else DevConfig
)
