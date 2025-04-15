@echo off
setlocal

REM Change to the directory containing this script
pushd %~dp0\..

echo Running from project root: %cd%

echo Creating virtual environment in .venv...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Upgrading pip...
pip install --upgrade pip

echo Installing project in editable mode with dev dependencies...
pip install -e .[dev]

echo Setup complete.
echo Remember to activate the environment next time with:
echo   .venv\Scripts\activate.bat
