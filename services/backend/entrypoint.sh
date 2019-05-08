#!/usr/bin/env bash

echo "Starting PostgreSQL"
while ! nc -z users-db 5432; do
    sleep 0.2
done

echo "PostgreSQL started"

gunicorn -b 0.0.0.0:5000 --log-level=debug --log-file /usr/src/app/gunicorn.log manage:app