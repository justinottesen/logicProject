$ErrorActionPreference = "Stop"

$REPO_ROOT = Resolve-Path "$PSScriptRoot\.."
$BACKEND = "$REPO_ROOT\backend"
$FRONTEND = "$REPO_ROOT\frontend"
$VENV = "$BACKEND\.venv"

# Step 1: Check backend venv
if (-not (Test-Path $VENV)) {
    Write-Host "Backend virtual environment not found, running setup..."
    & "$BACKEND\scripts\dev_setup.ps1"
}

# Step 2: Activate backend venv
Write-Host "Activating backend virtual environment..."
& "$VENV\Scripts\Activate.ps1"

# Step 3: Install frontend dependencies
Write-Host "Installing frontend dependencies..."
Set-Location $FRONTEND
npm install

# Step 4: Run backend and frontend in parallel
Write-Host "Starting backend and frontend..."

# Start both and capture jobs
$backend = Start-Job { proof_server --rules-dir "$REPO_ROOT\custom_rules"}
$frontend = Start-Job { npm run dev --prefix "$using:FRONTEND" }

# Clean up on Ctrl+C
$finished = $false
$onExit = {
    if (-not $finished) {
        Write-Host "`nStopping servers..."
        Stop-Job $backend
        Stop-Job $frontend
        Remove-Job $backend, $frontend -Force
        $finished = $true
    }
}
Register-EngineEvent PowerShell.Exiting -Action $onExit

Write-Host "Servers running. Press Ctrl+C to stop both."

# Wait for either to exit
while ($true) {
    Wait-Job -Job $backend, $frontend -Any | Out-Null
    break
}

& $onExit.Invoke()
