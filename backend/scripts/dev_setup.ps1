# Exit on any error
$ErrorActionPreference = "Stop"

# Go to backend root
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND_ROOT = Resolve-Path "$SCRIPT_DIR\.."
Set-Location $BACKEND_ROOT

Write-Host "Running from backend root: $BACKEND_ROOT"

# Create virtual environment
Write-Host "Creating virtual environment in .venv..."
python -m venv .venv
Write-Host "Virtual environment created."

# Activate virtual environment
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# Upgrade pip and install
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing backend in editable mode with dev dependencies..."
pip install -e .[dev]

Write-Host "Setup complete."
Write-Host "To activate next time, run:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
