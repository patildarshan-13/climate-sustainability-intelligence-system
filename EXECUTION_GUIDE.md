# Execution Guide - Climate & Sustainability Intelligence System

## ✅ Root Cause Fixed

**Primary Issue:** Missing `emergentintegrations` package (not available on PyPI)
**Solution:** Replaced with direct OpenAI API integration

**Secondary Issues Fixed:**
- FastAPI/Pydantic version mismatch
- MongoDB connection error handling
- Logger initialization order
- Dependency installation conflicts

## 🚀 Quick Start (Recommended)

### Windows PowerShell:

```powershell
.\run-project.ps1
```

This automated script handles everything.

## 📋 Manual Execution Steps

### Step 1: Environment Setup

**Backend** - Create/Edit `backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecointel
OPENAI_API_KEY=sk-your-openai-api-key-here
CORS_ORIGINS=http://localhost:3000
```

**Frontend** - Create/Edit `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Step 2: Install Dependencies

**Backend:**
```powershell
cd backend
python -m pip install fastapi uvicorn motor python-dotenv pymongo faiss-cpu sentence-transformers PyPDF2 tiktoken openai numpy scikit-learn
cd ..
```

**Frontend:**
```powershell
cd frontend
npm install --legacy-peer-deps
cd ..
```

### Step 3: Start MongoDB

**Option A - Local MongoDB:**
```powershell
# Check if running
Get-Service MongoDB

# If not running, start it
Start-Service MongoDB
```

**Option B - MongoDB Atlas (Cloud):**
1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `MONGO_URL` in `backend/.env`

### Step 4: Start Backend Server

**Terminal 1:**
```powershell
cd backend
python server.py
```

**Expected Output:**
```
INFO:     ============================================================
INFO:     Climate & Sustainability Intelligence System - Backend
INFO:     ============================================================
INFO:     MongoDB URL: mongodb://localhost:27017
INFO:     Database: ecointel
INFO:     API Key configured: Yes
INFO:     ============================================================
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Success Indicators:**
- ✅ No error messages
- ✅ "Uvicorn running on http://0.0.0.0:8000"
- ✅ Can access http://localhost:8000/api/

### Step 5: Start Frontend Server

**Terminal 2:**
```powershell
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Success Indicators:**
- ✅ "Compiled successfully!"
- ✅ Browser opens automatically to http://localhost:3000
- ✅ UI loads without errors

## ✅ Verification Tests

### Test 1: Backend API Health
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing
```

**Expected Response:**
```json
{"message": "EcoIntel API - Climate & Sustainability Intelligence"}
```

### Test 2: API Documentation
Open browser: http://localhost:8000/docs

**Expected:** Swagger UI with all API endpoints

### Test 3: Frontend UI
Open browser: http://localhost:3000

**Expected:**
- Homepage with "Upload Document" button
- Modern dark theme UI
- No console errors

### Test 4: End-to-End Flow

1. **Upload Document:**
   - Click "Upload Document"
   - Select a PDF/TXT/Markdown file
   - Wait for "Document uploaded and processed successfully"

2. **Query Document:**
   - Navigate to Dashboard → Query Interface
   - Type a question about the document
   - Click Send
   - Verify answer appears with source references

## 🎯 Success Criteria

### Backend Running Successfully:
- ✅ Server starts without errors
- ✅ MongoDB connection established (or graceful warning)
- ✅ API responds at http://localhost:8000/api/
- ✅ API docs accessible at http://localhost:8000/docs

### Frontend Running Successfully:
- ✅ Compiles without errors
- ✅ Opens in browser at http://localhost:3000
- ✅ No console errors
- ✅ UI renders correctly

### Full System Working:
- ✅ Can upload documents (PDF/TXT/Markdown)
- ✅ Documents process and appear in library
- ✅ Can query documents
- ✅ Answers include source references
- ✅ All API endpoints functional

## 🔧 Troubleshooting

### Backend Issues

**Error: "Missing required environment variables"**
- Solution: Create `backend/.env` from `backend/env.template`

**Error: "MongoDB connection failed"**
- Solution: Start MongoDB service or use MongoDB Atlas

**Error: "ImportError: cannot import name 'Undefined'"**
- Solution: `python -m pip install --upgrade fastapi`

**Port 8000 already in use:**
- Solution: Change port in `server.py` or kill process using port 8000

### Frontend Issues

**Error: "Cannot find module"**
- Solution: `cd frontend && npm install --legacy-peer-deps`

**Error: "Network Error" or CORS issues**
- Solution: Check `REACT_APP_BACKEND_URL` in `frontend/.env`
- Solution: Check `CORS_ORIGINS` in `backend/.env`

**Port 3000 already in use:**
- Solution: `PORT=3001 npm start` or kill process

### MongoDB Issues

**Connection timeout:**
- Local: Check MongoDB service is running
- Atlas: Verify IP whitelist includes your IP

**Authentication failed:**
- Check connection string format
- Verify username/password in connection string

## 📊 Project Structure

```
climate-sustainability-intelligence-system-main/
├── backend/
│   ├── .env                    # Backend configuration (create from env.template)
│   ├── server.py               # FastAPI server entry point
│   ├── document_processor.py  # Document processing logic
│   ├── rag_engine.py          # RAG query engine
│   ├── vector_store.py        # FAISS vector store
│   ├── data/                  # FAISS index storage
│   └── uploads/               # Uploaded documents
├── frontend/
│   ├── .env                   # Frontend configuration (create from env.template)
│   ├── package.json
│   └── src/                   # React source code
├── run-project.ps1            # Automated startup script
└── EXECUTION_GUIDE.md         # This file
```

## 🎓 Academic Submission Checklist

- ✅ All dependencies properly installed
- ✅ Environment files configured
- ✅ Backend server runs without errors
- ✅ Frontend server runs without errors
- ✅ Full end-to-end functionality verified
- ✅ No console errors or warnings
- ✅ API documentation accessible
- ✅ Code is clean and standardized
- ✅ All imports resolved
- ✅ Configuration files present

## 🎤 Interview Demonstration

**Demo Flow:**
1. Show backend server running (Terminal 1)
2. Show frontend server running (Terminal 2)
3. Open browser to http://localhost:3000
4. Upload a sample document
5. Show document processing
6. Query the document
7. Show answer with sources
8. Show API documentation at http://localhost:8000/docs

**Key Points to Highlight:**
- RAG (Retrieval-Augmented Generation) architecture
- Vector search with FAISS
- Document processing pipeline
- Modern React frontend
- FastAPI backend
- MongoDB integration

---

## ✅ Final Status

**Project Status:** ✅ READY FOR EXECUTION

**All Issues Resolved:**
- ✅ Dependencies installed
- ✅ Code standardized
- ✅ Configuration files created
- ✅ Error handling improved
- ✅ Documentation complete

**Ready to run with:** `.\run-project.ps1` or manual steps above

