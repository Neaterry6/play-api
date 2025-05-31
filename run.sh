#!/bin/sh

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Starting Gunicorn with eventlet worker..."

exec gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
