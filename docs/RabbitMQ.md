## How to use RabbitMQ as the message queue

### Make sure RabbitMQ is running with Docker
Make sure your COMPOSE_PROFILES environment variable is set to 'RabbitMQ', this ensures RabbitMQ runs when you run 
`docker-compose up`.

Alternatively, run 
```
./run_local.sh
```
To set this environment variable and run `docker-compose up`

### Set your Celery Broker URL
Create a `.env` file and add the following lines
```
CELERY_BROKER_URL='amqp://guest:guest@rabbitmq:5672/'
QUEUE_URL='amqp://guest:guest@rabbitmq:5672/'
```
If you have modified the port or the login credentials ensure this is reflected here.

### Set your Queue Name
In your `.env` file add the following line.
```
QUEUE_NAME='celery'
```

If you have done all these steps you should be set up to use RabbitMQ as your local email queue. 

Items will automatically be read off the queue by the celery worker, so you may wish to stop the worker process in order to inspect the queue.