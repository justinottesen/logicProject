#!/bin/bash
set -e

# Move to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

BACKEND_VENV="$REPO_ROOT/backend/.venv"

# Step 1: Set up backend if not yet done
if [ ! -d "$BACKEND_VENV" ]; then
    echo "Backend virtual environment not found, running setup..."
    bash "$REPO_ROOT/backend/scripts/dev_setup.sh"
fi

# Step 2: Activate virtual environment
echo "Activating backend virtual environment..."
source "$BACKEND_VENV/bin/activate"

# Step 3: Install frontend dependencies
echo "Installing frontend dependencies..."
cd "$REPO_ROOT/frontend"
npm install

# Step 4: Launch backend and frontend in parallel
echo "Starting backend (proof_server)..."
cd "$REPO_ROOT"
proof_server &
BACK_PID=$!

echo "Starting frontend (npm run dev)..."
cd "$REPO_ROOT/frontend"
npm run dev &
FRONT_PID=$!

# Handle Ctrl+C to cleanly stop both
trap "echo; echo 'Shutting down...'; kill $BACK_PID $FRONT_PID; wait" SIGINT

echo "Both servers running. Press Ctrl+C to stop."
wait
