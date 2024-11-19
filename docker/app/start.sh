#!/usr/bin/env bash
set -ex

sleep 2
poetry run alembic -c /app/storage/alembic.ini upgrade head

nginx
poetry run python /app/app.py
