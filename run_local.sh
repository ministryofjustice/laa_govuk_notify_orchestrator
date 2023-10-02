#!/bin/bash
export ENVIRONMENT=${1:-development}

# COMPOSE_PROFILES is used to set the docker compose profile
# If this is set to development then RabbitMQ will launch with the API
export COMPOSE_PROFILES=$ENVIRONMENT

echo "running environment $ENVIRONMENT"

docker-compose down --remove-orphans
docker-compose up --build
