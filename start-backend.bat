@echo off
echo Starting Backend Server...
cd backend
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file from .env.example
    pause
    exit /b 1
)
python server.py
pause

