#!/usr/bin/env bash
set -euo pipefail

echo "Starting frontend dev server..."
cd verdaterra-ui

if [ ! -d node_modules ]; then
  echo "Installing npm dependencies..."
  npm install
fi

echo "Running: npm run dev -- --host --port 5173"
npm run dev -- --host 0.0.0.0 --port 5173
