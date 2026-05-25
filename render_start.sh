#!/bin/sh
set -e

# Ensure spaCy model exists (safe no-op if already installed)
python -m spacy download en_core_web_sm || true

# Start the app
exec gunicorn app:app

