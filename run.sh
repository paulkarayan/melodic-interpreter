#!/bin/bash

# Irish Tune Variation Generator - Full Stack Startup
# Starts both FastAPI backend (port 8000) and Vite frontend (port 5173)

# Log files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="logs"
BACKEND_LOG="${LOG_DIR}/backend_${TIMESTAMP}.log"
FRONTEND_LOG="${LOG_DIR}/frontend_${TIMESTAMP}.log"
COMBINED_LOG="${LOG_DIR}/combined_${TIMESTAMP}.log"

# Create logs directory
mkdir -p "$LOG_DIR"

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "[INFO] Loaded environment variables from .env"
fi

echo "=========================================="
echo "Irish Tune Variation Generator"
echo "Starting Full Stack Application"
echo "=========================================="
echo ""
echo "Logs will be written to:"
echo "  Backend:  $BACKEND_LOG"
echo "  Frontend: $FRONTEND_LOG"
echo "  Combined: $COMBINED_LOG"
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
    echo "[CLEANUP] Logs saved to $LOG_DIR/"
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend with logging
echo "[BACKEND] Starting FastAPI server..."
source .venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000 2>&1 | tee -a "$BACKEND_LOG" "$COMBINED_LOG" | sed 's/^/[BACKEND] /' &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend with logging (if package.json exists)
if [ -f "package.json" ]; then
    echo "[FRONTEND] Starting Vite dev server..."
    npm run dev 2>&1 | tee -a "$FRONTEND_LOG" "$COMBINED_LOG" | sed 's/^/[FRONTEND] /' &
    FRONTEND_PID=$!
else
    echo "[INFO] No package.json found - running backend only"
    FRONTEND_PID=""
fi

echo ""
echo "✅ Server(s) started!"
echo "   Backend PID: $BACKEND_PID"
if [ -n "$FRONTEND_PID" ]; then
    echo "   Frontend PID: $FRONTEND_PID"
fi
echo ""
echo "Press Ctrl+C to stop server(s)"
echo ""
echo "Tail logs with:"
echo "  tail -f $BACKEND_LOG"
if [ -n "$FRONTEND_PID" ]; then
    echo "  tail -f $FRONTEND_LOG"
fi
echo "  tail -f $COMBINED_LOG"
echo ""

# Wait for processes
wait
