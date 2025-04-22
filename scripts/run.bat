@echo off
setlocal enabledelayedexpansion

REM Navigate to project root
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%\..

REM Setup variables
set REPO_ROOT=%CD%
set BACKEND_VENV=%REPO_ROOT%\backend\.venv

REM Check for virtual environment
if not exist "%BACKEND_VENV%" (
    echo Backend virtual environment not found. Running setup...
    call backend\scripts\dev_setup.bat
)

REM Activate virtual environment
echo Activating backend virtual environment...
call "%BACKEND_VENV%\Scripts\activate.bat"

REM Install frontend dependencies
echo Installing frontend dependencies...
cd /d "%REPO_ROOT%\frontend"
call npm install

REM Start backend
cd /d "%REPO_ROOT%\backend"
start "Backend" cmd /c proof_server

REM Start frontend
cd /d "%REPO_ROOT%\frontend"
start "Frontend" cmd /c npm run dev

echo.
echo Both backend and frontend are running in new terminal windows.
echo Press Ctrl+C to exit this window only. To stop everything:
echo - Close both spawned terminal windows, or
echo - Use Task Manager to end "proof_server" and "node" processes

pause >nul
