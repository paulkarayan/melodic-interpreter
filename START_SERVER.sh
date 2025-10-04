#!/bin/bash
# Start the Irish Tune Variation Generator server

echo "🎵 Starting Irish Tune Variation Generator..."
echo ""

# Activate uv environment and run server
source .venv/bin/activate
uvicorn app:app --reload --port 8000

echo ""
echo "Server running at http://localhost:8000"
echo "Press Ctrl+C to stop"
