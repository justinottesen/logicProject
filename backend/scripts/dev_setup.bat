@echo off
setlocal enabledelayedexpansion

REM Get directory of this script
set SCRIPT_DIR=%~dp0
pushd %SCRIPT_DIR%\..
set BACKEND_ROOT=%CD%

echo Running from backend root: %BACKEND_ROOT%

echo Creating virtual environment in .venv...
python -m venv .venv || goto :error

echo Virtual environment created.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip || goto :error

echo Installing backend in editable mode with dev dependencies...
pip install -e .[dev] || goto :error

echo Setup complete.
echo Remember to activate the environment next time with:
echo   call %BACKEND_ROOT%\venv\Scripts\activate.bat

goto :eof

:error
echo ERROR: Setup failed.
exit /b 1
