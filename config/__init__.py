import os
from .dev_config import DevConfig
from .staging_config import StagingConfig
from .prod_config import ProductionConfig

current_environment = os.environ.get("ENV", "development")

configs = {
    "development": DevConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}

config = configs[current_environment] if current_environment in configs else DevConfig
