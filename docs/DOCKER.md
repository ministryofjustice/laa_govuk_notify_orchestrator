## Running via Docker

```
docker build -t govuk_notify_orchestrator .

docker run -d --name govuk_notify_orchestrator -p 2500:2500 govuk_notify_orchestrator
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
