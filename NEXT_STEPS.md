# Next Steps - Getting the Application Running

## ✅ Step 1: Environment Files Created
The `.env` files have been created from templates. You need to edit them with your actual values.

## 📝 Step 2: Configure Backend Environment

Edit `backend/.env` and update these values:

1. **MONGO_URL**: 
   - Local MongoDB: `mongodb://localhost:27017` (default - keep if MongoDB is local)
   - MongoDB Atlas: Get connection string from https://www.mongodb.com/cloud/atlas
   - Example: `mongodb+srv://username:password@cluster.mongodb.net/`

2. **EMERGENT_LLM_KEY**: 
   - Replace `your_emergent_llm_api_key_here` with your actual API key
   - Get your key from Emergent Integrations

3. **CORS_ORIGINS**: 
   - Default is fine: `http://localhost:3000,http://localhost:3001`
   - Only change if frontend runs on different ports

## 📝 Step 3: Frontend Environment (Already Configured)
The `frontend/.env` is already set correctly for local development.

## 🔧 Step 4: Install Dependencies

### Backend Dependencies
```powershell
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### Frontend Dependencies
```powershell
cd frontend
npm install
cd ..
```

## 🗄️ Step 5: Start MongoDB

**Option A: Local MongoDB**
```powershell
# If MongoDB is installed as a service, it should already be running
# Check with: Get-Service MongoDB

# Or start manually:
mongod
```

**Option B: MongoDB Atlas (Cloud)**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get connection string
- Update `MONGO_URL` in `backend/.env`

## 🚀 Step 6: Start the Application

### Option A: Using Startup Scripts (Recommended)

**Terminal 1 - Backend:**
```powershell
.\start-backend.bat
```

**Terminal 2 - Frontend:**
```powershell
.\start-frontend.bat
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```powershell
.\venv\Scripts\Activate.ps1
cd backend
python server.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm start
```

## ✅ Step 7: Validate Setup

Before starting, run the validation script:
```powershell
python validate-setup.py
```

This will check:
- ✅ Python version
- ✅ Environment files
- ✅ Dependencies
- ✅ MongoDB connection

## 🌐 Step 8: Access the Application

Once both servers are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Step 9: Test the Application

1. Open http://localhost:3000 in your browser
2. Click "Upload Document" and upload a PDF/TXT/Markdown file
3. Wait for processing to complete
4. Navigate to Dashboard → Query Interface
5. Ask a question about your uploaded document

## ⚠️ Troubleshooting

### Backend won't start
- Check MongoDB is running: `mongosh` or check MongoDB service
- Verify `.env` file has correct `MONGO_URL`
- Check if port 8000 is available

### Frontend can't connect to backend
- Verify backend is running on http://localhost:8000
- Check `REACT_APP_BACKEND_URL` in `frontend/.env`
- Check CORS settings in `backend/.env`

### MongoDB connection error
- Verify MongoDB is running
- Check `MONGO_URL` in `backend/.env`
- For MongoDB Atlas, ensure IP is whitelisted

### Dependencies installation fails
- **Backend**: Make sure virtual environment is activated
- **Frontend**: Try `npm install --legacy-peer-deps` if there are peer dependency issues

## 📋 Quick Checklist

- [ ] Backend `.env` configured with MongoDB URL and API key
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend folder)
- [ ] MongoDB is running (local or Atlas)
- [ ] Validation script passes (`python validate-setup.py`)
- [ ] Backend server starts successfully
- [ ] Frontend server starts successfully
- [ ] Can access http://localhost:3000

---

**Ready to proceed?** Start with Step 2 (configure backend .env) and work through each step!

