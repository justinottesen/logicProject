@echo off
setlocal enabledelayedexpansion

REM Get directory of this script
set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%\..
set FRONTEND_ROOT=%CD%

echo Running from frontend root: %FRONTEND_ROOT%

where npm >nul 2>nul
if errorlevel 1 (
    echo ERROR: npm is not installed. Please install Node.js and npm first.
    exit /b 1
)

echo Installing frontend dependencies...
npm install || goto :error

echo Setup complete.
echo You can now start the frontend with:
echo   cd %FRONTEND_ROOT%
echo   npm run dev

goto :eof

:error
echo ERROR: Setup failed.
exit /b 1
