#!/bin/bash

set -e  # Exit on first error

# Get script and project directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$FRONTEND_ROOT"

echo "Running from frontend root: $FRONTEND_ROOT"

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

echo "Installing dependencies with npm..."
npm install

echo "Setup complete."
echo "You can now start the frontend with:"
echo "  cd '$FRONTEND_ROOT' && npm run dev"