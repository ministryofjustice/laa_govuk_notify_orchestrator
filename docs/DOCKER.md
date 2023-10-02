## How to start a docker version of the API (With RabbitMQ)

```
./run_local.sh
```

## How to start a docker version of the API (Without RabbitMQ)

```
docker-compose down --remove-orphans
docker-compose up
```

## Running unit testing in the docker container

Make sure the container is running with:

```
docker ps
```

Then execute the tests by running:

```
docker exec -it govuk_notify_orchestrator pytest
```
