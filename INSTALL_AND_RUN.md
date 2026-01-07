# Installation and Execution Guide

## Quick Start (Windows)

Run the automated setup script:

```powershell
.\run-project.ps1
```

This script will:
1. Check Python and Node.js
2. Create environment files
3. Install all dependencies
4. Start both servers

## Manual Setup

### Step 1: Prerequisites

- **Python 3.10+** installed
- **Node.js 18+** installed
- **MongoDB** running (local or Atlas)

### Step 2: Environment Configuration

**Backend** (`backend/.env`):
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecointel
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Step 3: Install Dependencies

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

### Step 4: Start MongoDB

**Local MongoDB:**
```powershell
# If installed as service, it should be running
# Check with: Get-Service MongoDB
```

**MongoDB Atlas (Cloud):**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string
- Update `MONGO_URL` in `backend/.env`

### Step 5: Run the Application

**Option A: Automated Script**
```powershell
.\run-project.ps1
```

**Option B: Manual Start**

Terminal 1 - Backend:
```powershell
cd backend
python server.py
```

Terminal 2 - Frontend:
```powershell
cd frontend
npm start
```

## Verification

### Backend Health Check

```powershell
# Check if backend is running
Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing
```

Expected response:
```json
{"message": "EcoIntel API - Climate & Sustainability Intelligence"}
```

### Frontend Access

Open browser: http://localhost:3000

### API Documentation

Open browser: http://localhost:8000/docs

## Success Indicators

✅ **Backend Running:**
- Terminal shows: "Uvicorn running on http://0.0.0.0:8000"
- No error messages
- Can access http://localhost:8000/api/

✅ **Frontend Running:**
- Terminal shows: "webpack compiled successfully"
- Browser opens to http://localhost:3000
- UI loads without errors

✅ **Full System Working:**
- Can upload documents (PDF/TXT/Markdown)
- Documents process successfully
- Can query documents and get answers
- Sources are displayed with answers

## Troubleshooting

### Backend won't start
- Check MongoDB is running
- Verify `.env` file exists and has correct values
- Check port 8000 is not in use

### Frontend can't connect
- Verify backend is running on port 8000
- Check `REACT_APP_BACKEND_URL` in `frontend/.env`
- Check CORS settings in `backend/.env`

### MongoDB connection error
- Verify MongoDB service is running
- Check `MONGO_URL` in `backend/.env`
- For Atlas, ensure IP is whitelisted

### Dependencies issues
- Backend: `python -m pip install --upgrade pip` then retry
- Frontend: `npm install --legacy-peer-deps --force`

## Project Structure

```
climate-sustainability-intelligence-system-main/
├── backend/
│   ├── .env                 # Backend configuration
│   ├── server.py            # FastAPI server
│   ├── document_processor.py
│   ├── rag_engine.py
│   ├── vector_store.py
│   └── requirements.txt
├── frontend/
│   ├── .env                 # Frontend configuration
│   ├── package.json
│   └── src/
├── run-project.ps1          # Automated startup script
└── INSTALL_AND_RUN.md       # This file
```

## Expected Output

### Backend Terminal:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Frontend Terminal:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

### Browser:
- Homepage with upload interface
- Dashboard with document library
- Query interface for asking questions

---

**Ready to use!** The application is now running and ready for document upload and querying.

