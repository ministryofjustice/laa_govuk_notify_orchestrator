from app import app
from app import logger


@app.on_event("startup")
async def startup_event():
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")
