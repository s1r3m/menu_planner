#!/usr/bin/env bash
set -ex

sleep 2
poetry run alembic -c /app/menu_planner/storage/alembic.ini upgrade head

nginx
poetry run python /app/menu_planner/app.py
