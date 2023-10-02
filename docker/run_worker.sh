#!/usr/bin/env sh
set -e
exec celery -A app.celery worker --concurrency=${WORKER_APP_CONCURRENCY:-4} --loglevel=${LOG_LEVEL:-INFO} --beat
