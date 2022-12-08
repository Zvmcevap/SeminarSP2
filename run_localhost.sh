#!/bin/sh

export APP_MODULE=${APP_MODULE-app.main:app}
export HOST=${HOST:-localhost}
export PORT=${PORT:-8000}

exec uvicorn --host "$HOST" --port "$PORT" --reload "$APP_MODULE"
