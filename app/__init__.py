from fastapi import FastAPI
from config import Config
from routers import router
import logging


app = FastAPI(
    title=Config.TITLE,
    summary=Config.SUMMARY,
    version=Config.VERSION,
    terms_of_service=Config.TERMS_OF_SERVICE,
    license_info=Config.LICENCE_INFO,
)

app.include_router(router)

logger = logging.getLogger("uvicorn")
