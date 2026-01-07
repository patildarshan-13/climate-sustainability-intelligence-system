# Frontend Problem - Complete Fix Guide

## Common Frontend Issues & Solutions

### Issue 1: "Cannot find module" or Missing Dependencies

**Solution:**
```powershell
cd frontend
rm -r node_modules  # If exists
npm install --legacy-peer-deps
```

**Verify:**
```powershell
Test-Path "node_modules"  # Should return True
```

---

### Issue 2: ".env file missing"

**Solution:**
```powershell
cd frontend
Copy-Item env.template .env
```

**Verify .env contains:**
```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

### Issue 3: "Port 3000 already in use"

**Solution:**
```powershell
# Find process using port 3000
Get-NetTCPConnection -LocalPort 3000 | Select-Object OwningProcess

# Kill the process (replace <PID> with actual process ID)
Stop-Process -Id <PID>

# Or use different port
$env:PORT=3001
npm start
```

---

### Issue 4: "ERR_CONNECTION_REFUSED" in Browser

**Causes:**
- Frontend server not started
- Still compiling (wait 30-60 seconds)
- Wrong URL

**Solution:**
```powershell
# 1. Start frontend server
cd frontend
npm start

# 2. Wait for "Compiled successfully!" message
# 3. Then open http://localhost:3000
```

---

### Issue 5: "npm start" fails with errors

**Common Errors:**

**Error: "Missing script: start"**
```powershell
# Check package.json has start script
Get-Content package.json | Select-String "start"
```

**Error: "Cannot find module 'react-scripts'"**
```powershell
npm install --legacy-peer-deps
```

**Error: "EADDRINUSE: address already in use"**
```powershell
# Kill process on port 3000
Get-NetTCPConnection -LocalPort 3000 | ForEach-Object { Stop-Process -Id $_.OwningProcess }
```

---

### Issue 6: Frontend can't connect to backend

**Check:**
1. Backend is running on http://localhost:8000
2. `frontend/.env` has: `REACT_APP_BACKEND_URL=http://localhost:8000`
3. CORS is configured in backend

**Solution:**
```powershell
# Verify backend is running
Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing

# If fails, start backend first
cd ..\backend
python server.py
```

---

## Complete Frontend Reset

If nothing works, do a complete reset:

```powershell
cd frontend

# 1. Remove node_modules and package-lock.json
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item package-lock.json -ErrorAction SilentlyContinue

# 2. Clear npm cache
npm cache clean --force

# 3. Reinstall dependencies
npm install --legacy-peer-deps

# 4. Verify .env exists
if (-not (Test-Path ".env")) {
    Copy-Item env.template .env
}

# 5. Start server
npm start
```

---

## Step-by-Step Frontend Startup

### Step 1: Navigate to Frontend
```powershell
cd C:\Users\darsh\Downloads\climate-sustainability-intelligence-system-main\climate-sustainability-intelligence-system-main\frontend
```

### Step 2: Verify Setup
```powershell
# Check files exist
Test-Path "package.json"
Test-Path ".env"
Test-Path "src\App.js"
```

### Step 3: Install Dependencies (if needed)
```powershell
npm install --legacy-peer-deps
```

### Step 4: Start Server
```powershell
npm start
```

### Step 5: Wait for Compilation
- First time: 30-60 seconds
- Look for: "Compiled successfully!"
- Browser opens automatically

### Step 6: Access Application
- URL: http://localhost:3000
- Should load without errors

---

## Verification Checklist

Before starting frontend, verify:

- [ ] In correct directory: `frontend/`
- [ ] `package.json` exists
- [ ] `.env` file exists with `REACT_APP_BACKEND_URL`
- [ ] `node_modules` exists (or run `npm install`)
- [ ] Port 3000 is available
- [ ] Backend is running on port 8000

---

## Quick Fix Command

**All-in-one fix:**
```powershell
cd frontend
if (-not (Test-Path ".env")) { Copy-Item env.template .env }
if (-not (Test-Path "node_modules")) { npm install --legacy-peer-deps }
npm start
```

---

## Expected Output

**Successful startup:**
```
Compiling...
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**If you see errors, check the specific error message and refer to solutions above.**

