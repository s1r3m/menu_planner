#!/usr/bin/env bash
set -ex

nginx
poetry run python /app/menu_planner/app.py
