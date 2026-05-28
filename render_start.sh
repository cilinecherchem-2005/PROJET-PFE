#!/bin/sh
set -e

# Render will run this script. We ensure dependencies/models exist.
# (no-op if already installed/cached)
python -m spacy download fr_core_news_sm || true

# Use Render-provided PORT when present.
PORT=${PORT:-5000}

# Start the app
# - use the Flask app object from app.py (app = create_app())
exec gunicorn app:app \
  --bind 0.0.0.0:${PORT} \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout 120


