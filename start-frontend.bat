@echo off
echo Starting Frontend Development Server...
cd frontend
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file from .env.example
    pause
    exit /b 1
)
call npm start
pause

