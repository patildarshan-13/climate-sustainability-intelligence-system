from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import shutil

from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_engine import RAGEngine

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Validate required environment variables
required_env_vars = ['MONGO_URL', 'DB_NAME']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. Please create a .env file.")

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
try:
    client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
    db = client[os.environ['DB_NAME']]
    logger.info(f"Connected to MongoDB: {os.environ['DB_NAME']}")
except Exception as e:
    logger.warning(f"MongoDB connection warning: {e}. Server will start but database operations may fail.")
    # Create a dummy client to prevent crashes
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]

# Initialize RAG components
document_processor = DocumentProcessor()
vector_store = VectorStore(dimension=384, index_path="./data/faiss_index")

rag_engine = RAGEngine(
    vector_store=vector_store,
    document_processor=document_processor
)


# Create upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Models
class Document(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_size: int
    file_type: str
    upload_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "processing"
    chunk_count: int = 0
    total_tokens: int = 0


class DocumentResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    status: str
    chunk_count: int
    total_tokens: int


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class QueryResponse(BaseModel):
    query_id: str
    question: str
    answer: str
    sources: List[dict]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Routes
@api_router.get("/")
async def root():
    return {"message": "EcoIntel API - Climate & Sustainability Intelligence"}


@api_router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.txt', '.md', '.markdown']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Save file
        file_path = UPLOAD_DIR / f"{doc_id}{file_ext}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create document record
        doc = Document(
            id=doc_id,
            filename=file.filename,
            file_size=file_size,
            file_type=file_ext,
            status="processing"
        )
        
        # Save to MongoDB
        doc_dict = doc.model_dump()
        doc_dict['upload_date'] = doc_dict['upload_date'].isoformat()
        await db.documents.insert_one(doc_dict)
        
        # Process document in background (async)
        try:
            processed = await document_processor.process_document(str(file_path))
            chunks = processed['chunks']
            
            # Generate embeddings for each chunk
            embeddings = []
            metadata_list = []
            
            for chunk in chunks:
                embedding = await document_processor.generate_embedding(chunk['text'])
                embeddings.append(embedding)
                metadata_list.append({
                    'doc_id': doc_id,
                    'filename': file.filename,
                    'chunk_index': chunk['chunk_index'],
                    'text': chunk['text'],
                    'token_count': chunk['token_count']
                })
            
            # Add to vector store
            vector_store.add_vectors(embeddings, metadata_list)
            
            # Update document status
            await db.documents.update_one(
                {"id": doc_id},
                {"$set": {
                    "status": "ready",
                    "chunk_count": len(chunks),
                    "total_tokens": processed['total_tokens']
                }}
            )
            
            doc.status = "ready"
            doc.chunk_count = len(chunks)
            doc.total_tokens = processed['total_tokens']
            
        except Exception as e:
            logging.error(f"Error processing document: {str(e)}")
            await db.documents.update_one(
                {"id": doc_id},
                {"$set": {"status": "error"}}
            )
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
        
        return doc
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/documents", response_model=List[DocumentResponse])
async def get_documents():
    """Get all documents"""
    try:
        docs = await db.documents.find({}, {"_id": 0}).sort("upload_date", -1).to_list(100)
        
        # Convert ISO strings back to datetime
        for doc in docs:
            if isinstance(doc['upload_date'], str):
                doc['upload_date'] = datetime.fromisoformat(doc['upload_date'])
        
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document"""
    try:
        # Check if document exists
        doc = await db.documents.find_one({"id": doc_id}, {"_id": 0})
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from vector store
        vector_store.delete_by_document_id(doc_id)
        
        # Delete file
        file_ext = doc['file_type']
        file_path = UPLOAD_DIR / f"{doc_id}{file_ext}"
        if file_path.exists():
            file_path.unlink()
        
        # Delete from database
        await db.documents.delete_one({"id": doc_id})
        
        return {"message": "Document deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using RAG"""
    try:
        # Check if there are any documents
        doc_count = await db.documents.count_documents({"status": "ready"})
        if doc_count == 0:
            return QueryResponse(
                query_id=str(uuid.uuid4()),
                question=request.question,
                answer="No documents available. Please upload documents first.",
                sources=[]
            )
        
        # Process query
        result = await rag_engine.query(request.question, top_k=request.top_k)
        
        # Save query to database
        query_doc = {
            "query_id": result['query_id'],
            "question": request.question,
            "answer": result['answer'],
            "sources": result['sources'],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.queries.insert_one(query_doc)
        
        return QueryResponse(
            query_id=result['query_id'],
            question=request.question,
            answer=result['answer'],
            sources=result['sources']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/queries", response_model=List[QueryResponse])
async def get_queries(limit: int = 20):
    """Get query history"""
    try:
        queries = await db.queries.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
        
        # Convert ISO strings back to datetime
        for query in queries:
            if isinstance(query.get('timestamp'), str):
                query['timestamp'] = datetime.fromisoformat(query['timestamp'])
        
        return queries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        doc_count = await db.documents.count_documents({})
        ready_count = await db.documents.count_documents({"status": "ready"})
        query_count = await db.queries.count_documents({})
        vector_count = vector_store.get_total_vectors()
        
        return {
            "total_documents": doc_count,
            "ready_documents": ready_count,
            "total_queries": query_count,
            "total_vectors": vector_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
