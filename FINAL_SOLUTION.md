# FINAL SOLUTION - Complete Project Execution Guide

## 🎯 COMPLETE STEP-BY-STEP SOLUTION

### STEP 1: Navigate to Correct Directory

```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main
```

**VERIFY:** You should see `backend` and `frontend` folders in current directory.

---

### STEP 2: Verify/Create Environment Files

**Backend (.env):**
```powershell
# If .env doesn't exist, create it
if (-not (Test-Path "backend\.env")) {
    Copy-Item "backend\env.template" "backend\.env"
}

# Edit backend\.env and set:
# MONGO_URL=mongodb://localhost:27017
# DB_NAME=ecointel
# OPENAI_API_KEY=your-openai-api-key-here
# CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env):**
```powershell
# If .env doesn't exist, create it
if (-not (Test-Path "frontend\.env")) {
    Copy-Item "frontend\env.template" "frontend\.env"
}

# frontend\.env should have:
# REACT_APP_BACKEND_URL=http://localhost:8000
```

---

### STEP 3: Install Backend Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn motor python-dotenv pymongo faiss-cpu sentence-transformers PyPDF2 tiktoken openai numpy scikit-learn
```

**Verify installation:**
```powershell
python -c "import fastapi, motor, faiss, sentence_transformers, openai; print('✅ All packages installed')"
```

---

### STEP 4: Install Frontend Dependencies

```powershell
cd frontend
npm install --legacy-peer-deps
cd ..
```

**Verify installation:**
```powershell
Test-Path "frontend\node_modules"  # Should return True
```

---

### STEP 5: Start MongoDB (Choose One)

**Option A - Local MongoDB:**
```powershell
# Check if running
Get-Service MongoDB

# If not running, start it
Start-Service MongoDB
```

**Option B - MongoDB Atlas (Cloud - Recommended):**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account and cluster
3. Get connection string
4. Update `MONGO_URL` in `backend\.env`

---

### STEP 6: Start Backend Server

**Open NEW PowerShell Window (Terminal 1):**

```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main\backend
python server.py
```

**Expected Output:**
```
INFO:     ============================================================
INFO:     Climate & Sustainability Intelligence System - Backend
INFO:     ============================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify Backend:**
```powershell
# In another terminal
Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing
```

**Should return:** `{"message": "EcoIntel API - Climate & Sustainability Intelligence"}`

---

### STEP 7: Start Frontend Server

**Open NEW PowerShell Window (Terminal 2):**

```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main\frontend
npm start
```

**Expected Output:**
```
Compiling...
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

**First compilation takes 30-60 seconds!**

---

### STEP 8: Access Application

1. **Frontend:** http://localhost:3000 (opens automatically)
2. **Backend API:** http://localhost:8000/api/
3. **API Docs:** http://localhost:8000/docs

---

## 🔧 TROUBLESHOOTING

### Backend Won't Start

**Error: "Missing required environment variables"**
```powershell
# Create .env file
Copy-Item "backend\env.template" "backend\.env"
# Then edit backend\.env with your values
```

**Error: "MongoDB connection failed"**
- Start MongoDB: `Start-Service MongoDB`
- Or use MongoDB Atlas and update `MONGO_URL` in `.env`

**Error: "Port 8000 already in use"**
```powershell
# Find and kill process
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
# Kill process (replace PID)
Stop-Process -Id <PID>
```

### Frontend Won't Start

**Error: "Cannot find module"**
```powershell
cd frontend
rm -r node_modules  # If exists
npm install --legacy-peer-deps
```

**Error: "Port 3000 already in use"**
```powershell
# Find and kill process
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess
# Kill process
Stop-Process -Id <PID>
```

**Error: "ERR_CONNECTION_REFUSED"**
- Wait 30-60 seconds for compilation
- Check terminal for "Compiled successfully!" message
- Then refresh browser

---

## ✅ VERIFICATION CHECKLIST

Before running, verify:

- [ ] In correct directory: `climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main`
- [ ] `backend\.env` exists and has MONGO_URL and OPENAI_API_KEY
- [ ] `frontend\.env` exists and has REACT_APP_BACKEND_URL
- [ ] Backend dependencies installed (fastapi, motor, etc.)
- [ ] Frontend dependencies installed (node_modules exists)
- [ ] MongoDB is running (local or Atlas)
- [ ] Ports 8000 and 3000 are available

---

## 🚀 QUICK START COMMANDS (Copy-Paste)

**Terminal 1 - Backend:**
```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main\backend
python server.py
```

**Terminal 2 - Frontend:**
```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main\frontend
npm start
```

**Wait 30-60 seconds, then open:** http://localhost:3000

---

## 📋 FINAL STATUS

**Project is ready to run!**

Follow the steps above in order. The most common issues are:
1. Wrong directory
2. Missing .env files
3. Dependencies not installed
4. MongoDB not running
5. Ports already in use

All solutions are provided above. Follow step-by-step and the project will run successfully.

---

**Last Updated:** Complete solution with all fixes applied.

