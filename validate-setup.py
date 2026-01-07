#!/usr/bin/env python3
"""
Setup validation script for Climate & Sustainability Intelligence System
Checks for required dependencies, environment files, and configuration
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.minor}")
    return True

def check_backend_env():
    """Check backend .env file"""
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        print("❌ Backend .env file not found")
        print("   Create it from backend/env.template")
        return False
    
    # Check required variables
    from dotenv import load_dotenv
    load_dotenv(backend_env)
    
    required = ['MONGO_URL', 'DB_NAME']
    missing = [var for var in required if not os.environ.get(var)]
    
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        return False
    
    print("✅ Backend .env file exists and has required variables")
    return True

def check_frontend_env():
    """Check frontend .env file"""
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        print("❌ Frontend .env file not found")
        print("   Create it from frontend/env.template")
        return False
    
    print("✅ Frontend .env file exists")
    return True

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    try:
        import fastapi
        import motor
        import faiss
        import sentence_transformers
        print("✅ Backend dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e.name}")
        print("   Run: pip install -r backend/requirements.txt")
        return False

def check_node_installed():
    """Check if Node.js is installed"""
    import subprocess
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed")
    print("   Install from: https://nodejs.org/")
    return False

def check_frontend_dependencies():
    """Check if frontend dependencies are installed"""
    node_modules = Path("frontend/node_modules")
    if not node_modules.exists():
        print("❌ Frontend dependencies not installed")
        print("   Run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies are installed")
    return True

def check_mongodb_connection():
    """Check MongoDB connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv(Path("backend/.env"))
        
        mongo_url = os.environ.get('MONGO_URL')
        if not mongo_url:
            print("⚠️  MONGO_URL not set, skipping MongoDB connection check")
            return True
        
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        async def test_connection():
            try:
                client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
                await client.admin.command('ping')
                client.close()
                return True
            except Exception:
                return False
        
        if asyncio.run(test_connection()):
            print("✅ MongoDB connection successful")
            return True
        else:
            print("⚠️  Could not connect to MongoDB")
            print("   Make sure MongoDB is running and MONGO_URL is correct")
            return False
    except Exception as e:
        print(f"⚠️  Could not check MongoDB connection: {e}")
        return True  # Don't fail validation for this

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("Climate & Sustainability Intelligence System - Setup Validation")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Backend Environment", check_backend_env),
        ("Frontend Environment", check_frontend_env),
        ("Backend Dependencies", check_backend_dependencies),
        ("Node.js Installation", check_node_installed),
        ("Frontend Dependencies", check_frontend_dependencies),
        ("MongoDB Connection", check_mongodb_connection),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            results.append(check_func())
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\nYou're ready to run the application!")
        print("Backend: cd backend && python server.py")
        print("Frontend: cd frontend && npm start")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\nPlease fix the issues above before running the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

