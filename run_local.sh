#!/bin/bash
export ENVIRONMENT=${1:-development}
export COMPOSE_PROFILES=$ENVIRONMENT
echo "running environment $ENVIRONMENT"
docker-compose down --remove-orphans
docker-compose up
