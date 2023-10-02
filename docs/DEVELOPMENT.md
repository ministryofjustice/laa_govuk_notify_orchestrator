# Development Guide

## How to start a local version of the API (with no message queue) 

```
python manage.py
```

## How to start a docker version of the API (With RabbitMQ)

```
./run_local.sh
```

## How to start a docker version of the API (Without RabbitMQ)

```
docker-compose down --remove-orphans
docker-compose up
```

## How do I run tests

Unit testing is performed using Pytest:

```
pytest
```
