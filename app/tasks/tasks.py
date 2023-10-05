from celery import current_app as app


@app.task(name='email:email_task')
def email_task(email):
    pass
