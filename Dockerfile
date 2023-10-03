FROM python:3.12

WORKDIR /notify_orchestrator

COPY ./requirements.txt /notify_orchestrator/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /notify_orchestrator/requirements.txt

COPY ./app /notify_orchestrator/app

COPY ./tests /notify_orchestrator/tests

COPY ./config /notify_orchestrator/config

COPY ./routers /notify_orchestrator/routers

COPY ./models /notify_orchestrator/models

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8026"]