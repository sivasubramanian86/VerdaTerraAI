#!/usr/bin/env bash
set -euo pipefail

echo "Starting backend services..."

# Ensure dependencies are installed (optional)
if [ -f requirements.txt ]; then
  echo "(Tip) install Python deps: pip install -r requirements.txt"
fi

# Export PYTHONPATH so verdaterrakai package can be imported
export PYTHONPATH="$(pwd)/verdaterrakai/src"

echo "Starting ingress API on http://localhost:8080"
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8080 &
INGRESS_PID=$!

echo "Starting agent API on http://localhost:8081"
uvicorn verdaterrakai.app.main:app --reload --host 0.0.0.0 --port 8081 &
AGENT_PID=$!

echo "Ingress PID: $INGRESS_PID, Agent PID: $AGENT_PID"
echo "Press Ctrl+C to stop"

wait $INGRESS_PID $AGENT_PID
