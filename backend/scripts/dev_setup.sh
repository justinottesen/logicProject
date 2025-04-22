#!/bin/bash

set -e  # Exit on first error

# Get directory of this script, then go to the backend root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BACKEND_ROOT"

echo "Running from backend root: $BACKEND_ROOT"

echo "Creating virtual environment in .venv..."
python3 -m venv .venv

echo "Virtual environment created."

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing backend in editable mode with dev dependencies..."
pip install -e ".[dev]"

echo "Setup complete."
echo "Remember to activate the environment next time with:"
echo "  source '$BACKEND_ROOT/.venv/bin/activate'"
