#!/usr/bin/env bash
set -euo pipefail

# Simple local runner for Investify
# - Creates a venv in .venv
# - Installs dependencies
# - Starts the Flask app on http://127.0.0.1:5000

cd "$(dirname "$0")"

PY=python3
if ! command -v $PY >/dev/null 2>&1; then
  echo "python3 not found. Please install Python 3.9+" >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "Creating virtual environment (.venv)..."
  $PY -m venv .venv
  echo "Activating virtual environment..."
  source .venv/bin/activate
  echo "Installing dependencies (first run)..."
  pip install -r requirements.txt
else
  echo "Activating virtual environment..."
  source .venv/bin/activate
  echo "Skipping pip upgrade and reinstall (use: RUN_INSTALL=1 to force)"
  if [ "${RUN_INSTALL:-0}" = "1" ]; then
    echo "Forcing dependency install..."
    pip install -r requirements.txt
  fi
fi

export FLASK_APP=app.py
export FLASK_ENV=production
# Default to 5002 to avoid common collisions on 5000; can be overridden via PORT env var
export PORT=${PORT:-5002}

echo "Checking if port $PORT is free..."
if lsof -i :"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  PID=$(lsof -i :"$PORT" -sTCP:LISTEN -t | head -n1)
  echo "Port $PORT is in use by PID $PID. Killing it..."
  kill -9 "$PID" || true
fi

echo "Starting server at http://127.0.0.1:$PORT ..."
exec python app.py


