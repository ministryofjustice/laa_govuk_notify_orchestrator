from fastapi import FastAPI
from config import Config
from routers import routers
from app.celery import create_celery
from app.lifespan import lifespan


def create_app():
    app = FastAPI(
        title=Config.TITLE,
        summary=Config.SUMMARY,
        version=Config.VERSION,
        terms_of_service=Config.TERMS_OF_SERVICE,
        license_info=Config.LICENCE_INFO,
        lifespan=lifespan
    )

    app.celery_app = create_celery()

    for router in routers:
        app.include_router(router)

    return app
