#!/usr/bin/env bash
# Starts the API and the web app in the background. Logs go to /tmp/ems-*.log.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! curl -sf http://localhost:8000/health >/dev/null; then
  (cd backend && setsid nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 >/tmp/ems-backend.log 2>&1 &)
fi
if ! curl -sf http://localhost:5173 >/dev/null; then
  (cd frontend && setsid nohup npm run dev -- --host 0.0.0.0 >/tmp/ems-frontend.log 2>&1 &)
fi

for _ in $(seq 1 30); do
  curl -sf http://localhost:8000/health >/dev/null && curl -sf http://localhost:5173 >/dev/null && break
  sleep 1
done

cat <<'MSG'

  Employee Management System is running.
    Web app:  port 5173 (opens in a new browser tab; see the PORTS panel for the URL)
    API docs: port 8000, path /docs
    Sign in:  admin / admin123

MSG
