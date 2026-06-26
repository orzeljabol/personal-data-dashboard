@echo off
cd /d "%~dp0"

start "VS Code" code .

start "Backend - FastAPI" powershell -NoExit -ExecutionPolicy Bypass -Command ".\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8001"

start "Frontend - React" powershell -NoExit -Command "cd frontend; npm run dev"


