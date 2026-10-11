#!/usr/bin/env bash
# Installs dependencies and prepares the database. Runs once when the container is created.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p /workspaces/.ems
pip install --no-cache-dir -r backend/requirements-dev.txt
(cd backend && alembic upgrade head)
(cd frontend && npm ci)
