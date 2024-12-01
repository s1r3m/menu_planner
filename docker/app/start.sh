#!/usr/bin/env bash
set -ex

poetry run alembic -c /migrations/alembic.ini upgrade head

nginx
cd .. && poetry run gunicorn -w 1 -b "0.0.0.0:8000" "app:app"
