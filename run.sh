#!/bin/bash

# Irish Tune Variation Generator - Full Stack Startup
# Starts both FastAPI backend (port 8000) and Vite frontend (port 5173)

echo "=========================================="
echo "Irish Tune Variation Generator"
echo "Starting Full Stack Application"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found at .venv"
    echo "Please create it first: python -m venv .venv"
    exit 1
fi

# Check for node_modules
if [ ! -d "node_modules" ]; then
    echo "[SETUP] Installing npm dependencies..."
    npm install
fi

# Check for Anthropic API
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "[WARNING] ANTHROPIC_API_KEY not set - Style Transformations disabled"
else
    echo "[INFO] ANTHROPIC_API_KEY found - Style Transformations enabled"
fi

echo ""
echo "=========================================="
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo "=========================================="
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "[CLEANUP] Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "[BACKEND] Starting FastAPI server..."
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000 2>&1 | sed 's/^/[BACKEND] /' &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "[FRONTEND] Starting Vite dev server..."
npm run dev 2>&1 | sed 's/^/[FRONTEND] /' &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers started!"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait
