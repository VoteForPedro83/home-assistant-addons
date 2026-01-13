#!/usr/bin/env sh
set -e

echo "Starting Git Bridge API..."

exec uvicorn app:app --host 0.0.0.0 --port 8000
