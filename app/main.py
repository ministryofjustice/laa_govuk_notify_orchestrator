from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config import Config
from routers import routers
import logging

logger = logging.getLogger("uvicorn")

app = FastAPI(
    title=Config.TITLE,
    summary=Config.SUMMARY,
    version=Config.VERSION,
    terms_of_service=Config.TERMS_OF_SERVICE,
    license_info=Config.LICENCE_INFO,
)

for router in routers:
    app.include_router(router)


@app.on_event("startup")
def on_startup():
    logger.info(f"Documentation can be found at the {app.docs_url} "
                f"or {app.redoc_url} endpoints.")


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <title>Not Found</title>
        <body>
            <h1>Not Found</h1>
            <p>The requested resource was not found on this server.</p>
        </body>
        </html>
    """)


@app.exception_handler(405)
async def custom_405_handler(_, __):
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <title>Not Allowed</title>
        <body>
            <h1>Not Allowed</h1>
            <p>The requested resource does not allow that method.</p>
        </body>
        </html>
    """)
