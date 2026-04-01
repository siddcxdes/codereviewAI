#!/bin/bash

echo "Starting FastAPI backend on port 8000..."
uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "Starting frontend web server on port 3000..."
python3 -m http.server 3000 -d frontend &
FRONTEND_PID=$!

echo ""
echo "🚀 CodeReview AI is successfully running local instances!"
echo "➡️  Frontend: http://localhost:3000"
echo "➡️  Backend:  http://localhost:8000"
echo ""
echo "Press [CTRL+C] to stop both services."

# Cleanup function to kill background processes when stopping the script
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Trap SIGINT (Ctrl+C) and trigger cleanup
trap cleanup SIGINT

# Wait continuously
wait
