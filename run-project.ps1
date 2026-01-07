# Climate & Sustainability Intelligence System - Startup Script
# This script sets up and runs the entire project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Climate & Sustainability Intelligence" -ForegroundColor Cyan
Write-Host "System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ $pythonVersion" -ForegroundColor Green

# Check Node.js
Write-Host "[2/6] Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Node.js not found!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Node.js $nodeVersion" -ForegroundColor Green

# Check environment files
Write-Host "[3/6] Checking environment files..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.env")) {
    Write-Host "  Creating backend/.env from template..." -ForegroundColor Yellow
    Copy-Item "backend\env.template" "backend\.env"
    Write-Host "  ⚠ Please edit backend/.env and set your OPENAI_API_KEY" -ForegroundColor Yellow
}
if (-not (Test-Path "frontend\.env")) {
    Write-Host "  Creating frontend/.env from template..." -ForegroundColor Yellow
    Copy-Item "frontend\env.template" "frontend\.env"
}
Write-Host "  ✓ Environment files ready" -ForegroundColor Green

# Install backend dependencies
Write-Host "[4/6] Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
python -m pip install --quiet --upgrade pip
python -m pip install fastapi uvicorn motor python-dotenv pymongo faiss-cpu sentence-transformers PyPDF2 tiktoken openai numpy scikit-learn --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Failed to install backend dependencies" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Write-Host "  ✓ Backend dependencies installed" -ForegroundColor Green
Set-Location ..

# Install frontend dependencies
Write-Host "[5/6] Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
if (-not (Test-Path "node_modules")) {
    npm install --legacy-peer-deps --silent
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Failed to install frontend dependencies" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
}
Write-Host "  ✓ Frontend dependencies installed" -ForegroundColor Green
Set-Location ..

# Start servers
Write-Host "[6/6] Starting servers..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting Backend Server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "Starting Frontend Server on http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python server.py" -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start" -WindowStyle Normal

Write-Host "✓ Servers starting in separate windows" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

