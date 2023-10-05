from app import celery as app


@app.task
def email_task():
    pass
