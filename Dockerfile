FROM python:3.12.3-alpine3.18

ENV CURL_VERSION=7.86.0
ENV PYCURL_SSL_LIBRARY=openssl
ENV SSL_VERSION=3.0.7

RUN apk add --no-cache --virtual .build-dependencies build-base curl-dev \
    && pip install pycurl

RUN apk add tzdata \ 
            libcurl \
            bash

RUN adduser -D app && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime

WORKDIR /notify_orchestrator

COPY ./requirements/generated/requirements.txt /notify_orchestrator/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /notify_orchestrator/requirements.txt

COPY ./app /notify_orchestrator/app

COPY ./bin /notify_orchestrator/bin

COPY ./tests /notify_orchestrator/tests

COPY ./config /notify_orchestrator/config

COPY ./routers /notify_orchestrator/routers

COPY ./models /notify_orchestrator/models

COPY ./utils /notify_orchestrator/utils

COPY manage.py /notify_orchestrator/manage.py

USER 1000

CMD ["uvicorn", "app.__init__:notify_orchestrator_api", "--host", "0.0.0.0", "--port", "8026"]