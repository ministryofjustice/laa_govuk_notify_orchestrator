FROM python:3.11.5-alpine3.18

RUN apk add tzdata \ 
            bash

RUN adduser -D app && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime

WORKDIR /notify_orchestrator

COPY ./requirements.txt /notify_orchestrator/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /notify_orchestrator/requirements.txt

COPY ./app /notify_orchestrator/app

COPY ./bin /notify_orchestrator/bin

COPY ./tests /notify_orchestrator/tests

COPY ./config /notify_orchestrator/config

COPY ./routers /notify_orchestrator/routers

COPY ./models /notify_orchestrator/models

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8026"]