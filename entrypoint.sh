#!/bin/sh

set -e

# Wait for database to be ready
echo "Waiting for postgres..."
while ! nc -z todo-db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
python manage.py makemigrations
python manage.py migrate

exec gunicorn todo.asgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker
