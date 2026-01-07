# Climate & Sustainability Intelligence System

An AI-powered document intelligence platform for analyzing ESG disclosures, carbon reports, and policy documents using Retrieval-Augmented Generation (RAG).
Architecture: React frontend → FastAPI backend → RAG pipeline (SentenceTransformers + FAISS + Hugging Face LLM) → MongoDB


## 🚀 Features

- **Document Upload & Processing**: Upload PDF, TXT, and Markdown files
- **RAG-Powered Querying**: Ask questions in natural language and get context-aware answers
- **Vector Search**: Fast semantic search using FAISS
- **Source References**: Every answer includes references to source document sections
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (for backend)
- **Node.js 18+** and **npm** or **yarn** (for frontend)
- **MongoDB** (local or cloud instance)
- No paid API keys required (uses local open-source Hugging Face models)

## 🛠️ Setup Instructions

### 1. Clone and Navigate to Project

```bash
cd climate-sustainability-intelligence-system
```

### 2. Backend Setup

#### Step 1: Create Virtual Environment (if not already created)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Edit `.env` and set the following variables:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecointel
CORS_ORIGINS=http://localhost:3000

```

#### Step 4: Start MongoDB

Make sure MongoDB is running on your system:

```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas (cloud) and update MONGO_URL accordingly
```

### 3. Frontend Setup

#### Step 1: Install Dependencies

```bash
cd frontend
npm install
# or
yarn install
```

#### Step 2: Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
cp .env.example .env
```

Edit `.env` and set:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

## 🏃 Running the Application

### Option 1: Manual Start (Recommended for Development)

#### Terminal 1 - Backend Server

```bash
cd backend
python server.py
```

The backend will start on `http://localhost:8000`

#### Terminal 2 - Frontend Development Server

```bash
cd frontend
npm start
# or
yarn start
```

The frontend will start on `http://localhost:3000`

### Option 2: Using Startup Scripts

#### Windows

```bash
# Backend
.\start-backend.bat

# Frontend (in a new terminal)
.\start-frontend.bat
```

#### Linux/Mac

```bash
# Backend
chmod +x start-backend.sh
./start-backend.sh

# Frontend (in a new terminal)
chmod +x start-frontend.sh
./start-frontend.sh
```

## 📖 Usage

1. **Access the Application**: Open `http://localhost:3000` in your browser
2. **Upload Documents**: Click "Upload Document" and select PDF, TXT, or Markdown files
3. **Query Documents**: Navigate to the Dashboard and use the Query Interface to ask questions
4. **View Results**: Answers include source references to the original documents

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest backend_test.py -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📁 Project Structure

```
climate-sustainability-intelligence-system
├── backend/
│   ├── data/              # FAISS index and metadata
│   ├── uploads/           # Uploaded documents
│   ├── document_processor.py
│   ├── rag_engine.py
│   ├── vector_store.py
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── ...
│   ├── package.json
│   └── .env
└── README.md
```

## 🔧 Troubleshooting

### Backend Issues

1. **MongoDB Connection Error**
   - Verify MongoDB is running: `mongosh` or check MongoDB service
   - Check `MONGO_URL` in `.env` file
   - For MongoDB Atlas, ensure IP whitelist includes your IP

2. **Missing Dependencies**
   - Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
   - Reinstall: `pip install -r requirements.txt`

3. **FAISS Installation Issues**
   - On Windows, you may need: `pip install faiss-cpu`
   - On Mac M1/M2: `pip install faiss-cpu` (CPU version recommended)

4. **LLM Configuration**
   - This project uses fully local Hugging Face models by default
   - No external API keys are required to run the system


### Frontend Issues

1. **Backend Connection Error**
   - Verify backend is running on `http://localhost:8000`
   - Check `REACT_APP_BACKEND_URL` in frontend `.env`
   - Check CORS settings in backend `.env`

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Clear cache: `npm start -- --reset-cache`

3. **Port Already in Use**
   - Change port: `PORT=3001 npm start`
   - Or kill process using port 3000

## 🚀 Production Readiness Improvements

### Security

- [ ] Add authentication and authorization (JWT tokens)
- [ ] Implement rate limiting for API endpoints
- [ ] Add input validation and sanitization
- [ ] Use environment-specific configuration files
- [ ] Enable HTTPS in production
- [ ] Add API key rotation mechanism

### Performance

- [ ] Implement caching for frequently accessed documents
- [ ] Add database connection pooling
- [ ] Optimize vector search with FAISS index types (IVF, HNSW)
- [ ] Add pagination for document and query lists
- [ ] Implement background job processing (Celery, RQ)

### Monitoring & Logging

- [ ] Add structured logging (JSON format)
- [ ] Implement health check endpoints
- [ ] Add application performance monitoring (APM)
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Add metrics collection (Prometheus, Grafana)

### Scalability

- [ ] Containerize with Docker
- [ ] Add Kubernetes deployment manifests
- [ ] Implement horizontal scaling for backend
- [ ] Use managed MongoDB (Atlas) or Redis for caching
- [ ] Add load balancing

### Data Management

- [ ] Implement document versioning
- [ ] Add backup and restore functionality
- [ ] Set up automated data retention policies
- [ ] Add document access controls
- [ ] Implement audit logging

### Testing

- [ ] Add unit tests for all modules
- [ ] Add integration tests
- [ ] Add end-to-end tests (Cypress, Playwright)
- [ ] Set up CI/CD pipeline
- [ ] Add code coverage reporting

### Documentation

- [ ] Add API documentation (OpenAPI/Swagger)
- [ ] Create deployment guides
- [ ] Add architecture diagrams
- [ ] Document environment variables
- [ ] Add troubleshooting guide

## 📝 Environment Variables Reference

### Backend (.env)

| Variable | Description | Required | Default |
|--------|------------|----------|---------|
| MONGO_URL | MongoDB connection string | Yes | - |
| DB_NAME | Database name | Yes | ecointel |
| CORS_ORIGINS | Allowed CORS origins | No | * |


### Frontend (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `REACT_APP_BACKEND_URL` | Backend API URL | Yes | `http://localhost:8000` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the Troubleshooting section above
- Review the code comments
- Open an issue on the repository

---

**Built with ❤️ for Climate & Sustainability Intelligence**
