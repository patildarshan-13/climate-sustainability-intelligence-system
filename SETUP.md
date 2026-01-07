# Quick Setup Guide

## Step-by-Step Setup Instructions

### 1. Backend Environment Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create `.env` file from template:
   ```bash
   # Windows
   copy env.template .env
   
   # Linux/Mac
   cp env.template .env
   ```

3. Edit `.env` file and set your values:
   ```env
   MONGO_URL=mongodb://localhost:27017
   DB_NAME=ecointel
   EMERGENT_LLM_KEY=your_actual_api_key_here
   CORS_ORIGINS=http://localhost:3000
   ```

### 2. Frontend Environment Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create `.env` file from template:
   ```bash
   # Windows
   copy env.template .env
   
   # Linux/Mac
   cp env.template .env
   ```

3. Edit `.env` file (usually no changes needed if backend runs on default port):
   ```env
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```

### 3. Install Dependencies

#### Backend:
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend:
```bash
cd frontend
npm install
# or
yarn install
```

### 4. Start MongoDB

Make sure MongoDB is running:

**Windows:**
- If installed as service, it should start automatically
- Or run: `mongod` in a terminal

**Linux/Mac:**
```bash
# If installed via Homebrew
brew services start mongodb-community

# Or manually
mongod
```

**Or use MongoDB Atlas (Cloud):**
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a cluster and get connection string
- Update `MONGO_URL` in backend `.env`

### 5. Run the Application

#### Option A: Using Startup Scripts

**Windows:**
```bash
# Terminal 1 - Backend
start-backend.bat

# Terminal 2 - Frontend
start-frontend.bat
```

**Linux/Mac:**
```bash
# Terminal 1 - Backend
chmod +x start-backend.sh
./start-backend.sh

# Terminal 2 - Frontend
chmod +x start-frontend.sh
./start-frontend.sh
```

#### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 6. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (FastAPI auto-generated docs)

## Verification Checklist

- [ ] MongoDB is running and accessible
- [ ] Backend `.env` file is created with correct values
- [ ] Frontend `.env` file is created
- [ ] All Python dependencies installed
- [ ] All Node.js dependencies installed
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Can access http://localhost:3000 in browser

## Common Issues

### "Module not found" errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### "Cannot connect to MongoDB"
- Check MongoDB is running: `mongosh` or `mongo`
- Verify `MONGO_URL` in `.env` is correct
- For MongoDB Atlas, check IP whitelist

### "CORS error" in browser
- Check `CORS_ORIGINS` in backend `.env` includes frontend URL
- Restart backend server after changing `.env`

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check `REACT_APP_BACKEND_URL` in frontend `.env`
- Restart frontend after changing `.env`

