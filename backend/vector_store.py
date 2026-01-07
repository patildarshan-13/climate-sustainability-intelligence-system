import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple
from pathlib import Path

class VectorStore:
    def __init__(self, dimension: int = 384, index_path: str = "./data/faiss_index"):
        self.dimension = dimension
        self.index_path = Path(index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize FAISS index (using L2 distance)
        self.index = faiss.IndexFlatL2(dimension)
        
        # Store metadata for each vector
        self.metadata = []
        
        # Load existing index if available
        self.load_index()
    
    def add_vectors(self, vectors: List[List[float]], metadata_list: List[Dict]):
        """Add vectors to the index with metadata"""
        vectors_array = np.array(vectors, dtype=np.float32)
        self.index.add(vectors_array)
        self.metadata.extend(metadata_list)
        self.save_index()
    
    def search(self, query_vector: List[float], k: int = 5) -> List[Dict]:
        """Search for k nearest neighbors"""
        if self.index.ntotal == 0:
            return []
        
        # Ensure k doesn't exceed total vectors
        k = min(k, self.index.ntotal)
        
        query_array = np.array([query_vector], dtype=np.float32)
        distances, indices = self.index.search(query_array, k)
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            # FAISS returns -1 for invalid indices when k > ntotal
            if idx >= 0 and idx < len(self.metadata):
                result = {
                    "distance": float(distance),
                    "rank": i + 1,
                    **self.metadata[idx]
                }
                results.append(result)
        
        return results
    
    def delete_by_document_id(self, doc_id: str):
        """Delete all vectors associated with a document"""
        # Filter metadata
        indices_to_keep = [i for i, meta in enumerate(self.metadata) if meta.get('doc_id') != doc_id]
        
        if len(indices_to_keep) == len(self.metadata):
            return  # No vectors to delete
        
        # Rebuild index with remaining vectors
        remaining_metadata = [self.metadata[i] for i in indices_to_keep]
        
        # Create new index
        new_index = faiss.IndexFlatL2(self.dimension)
        
        # Extract vectors from old index one by one
        if len(indices_to_keep) > 0:
            remaining_vectors = []
            for idx in indices_to_keep:
                vector = self.index.reconstruct(int(idx))
                remaining_vectors.append(vector)
            
            if remaining_vectors:
                vectors_array = np.array(remaining_vectors, dtype=np.float32)
                new_index.add(vectors_array)
        
        self.index = new_index
        self.metadata = remaining_metadata
        self.save_index()
    
    def save_index(self):
        """Save index and metadata to disk"""
        faiss.write_index(self.index, str(self.index_path / "index.faiss"))
        with open(self.index_path / "metadata.pkl", 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load_index(self):
        """Load index and metadata from disk"""
        index_file = self.index_path / "index.faiss"
        metadata_file = self.index_path / "metadata.pkl"
        
        if index_file.exists() and metadata_file.exists():
            self.index = faiss.read_index(str(index_file))
            with open(metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
    
    def get_total_vectors(self) -> int:
        """Get total number of vectors in index"""
        return self.index.ntotal
