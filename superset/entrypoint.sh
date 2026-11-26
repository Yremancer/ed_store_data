#!/usr/bin/env bash
set -euo pipefail

superset db upgrade
superset init
python /app/ed-store/bootstrap.py

exec /app/docker/entrypoints/run-server.sh
