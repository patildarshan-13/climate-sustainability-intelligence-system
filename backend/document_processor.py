import PyPDF2
import tiktoken
import os
from typing import List, Dict
from pathlib import Path
import asyncio
from sentence_transformers import SentenceTransformer

class DocumentProcessor:
    def __init__(self):
        pass

        self.encoding = tiktoken.get_encoding("cl100k_base")
        # Use sentence-transformers for embeddings (384 dimensions)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def extract_text_from_markdown(self, md_path: str) -> str:
        """Extract text from Markdown file"""
        return self.extract_text_from_txt(md_path)
    
    def extract_text(self, file_path: str) -> str:
        """Extract text based on file extension"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.txt':
            return self.extract_text_from_txt(file_path)
        elif file_ext in ['.md', '.markdown']:
            return self.extract_text_from_markdown(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, any]]:
        """Chunk text into smaller pieces with overlap"""
        tokens = self.encoding.encode(text)
        chunks = []
        
        start = 0
        chunk_index = 0
        
        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunks.append({
                "text": chunk_text,
                "chunk_index": chunk_index,
                "token_count": len(chunk_tokens)
            })
            
            start += chunk_size - overlap
            chunk_index += 1
        
        return chunks
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using sentence-transformers"""
        try:
            # Encode text to get embedding (runs in executor to avoid blocking)
            import concurrent.futures
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                embedding = await loop.run_in_executor(
                    pool, 
                    self.embedding_model.encode, 
                    text
                )
            return embedding.tolist()
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    async def process_document(self, file_path: str) -> Dict:
        """Process document: extract text and create chunks"""
        try:
            text = self.extract_text(file_path)
            chunks = self.chunk_text(text)
            
            return {
                "full_text": text,
                "chunks": chunks,
                "total_tokens": self.count_tokens(text),
                "chunk_count": len(chunks)
            }
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
