## Running via Docker
```
docker build -t govuk_notify_orchestrator .  

docker run -d --name govuk_notify_orchestrator -p 2500:2500 govuk_notify_orchestrator
```