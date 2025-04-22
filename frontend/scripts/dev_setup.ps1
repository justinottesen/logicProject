$ErrorActionPreference = "Stop"

# Go to frontend root
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$FRONTEND_ROOT = Resolve-Path "$SCRIPT_DIR\.."
Set-Location $FRONTEND_ROOT

Write-Host "Running from frontend root: $FRONTEND_ROOT"

# Check for npm
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm is not installed. Please install Node.js and npm first."
    exit 1
}

# Install dependencies
Write-Host "Installing frontend dependencies..."
npm install

Write-Host "Setup complete."
Write-Host "You can now start the frontend with:"
Write-Host "  cd `"$FRONTEND_ROOT`""
Write-Host "  npm run dev"
