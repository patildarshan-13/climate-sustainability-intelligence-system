from typing import List, Dict
import uuid
from transformers import pipeline


class RAGEngine:
    def __init__(self, vector_store, document_processor):
        self.vector_store = vector_store
        self.document_processor = document_processor

        # Hugging Face local model (FREE)
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1  # CPU
        )

        self.system_prompt = (
            "You are an AI assistant specialized in analyzing sustainability and "
            "climate-related documents. Answer questions strictly based on the "
            "provided context. If the answer is not present, say: "
            "'The document does not contain this information.'"
        )

    async def query(self, question: str, top_k: int = 5) -> Dict:
        try:
            # Generate embedding
            question_embedding = await self.document_processor.generate_embedding(question)

            # Retrieve chunks
            retrieved_chunks = self.vector_store.search(question_embedding, k=top_k)

            if not retrieved_chunks:
                return {
                    "answer": "No relevant documents found.",
                    "sources": [],
                    "query_id": str(uuid.uuid4())
                }

            context = self._format_context(retrieved_chunks)

            answer = self._generate_answer(question, context)
            sources = self._format_sources(retrieved_chunks)

            return {
                "answer": answer,
                "sources": sources,
                "query_id": str(uuid.uuid4())
            }

        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "query_id": str(uuid.uuid4())
            }

    def _format_context(self, chunks: List[Dict]) -> str:
        context_parts = []
        for chunk in chunks:
            context_parts.append(
                f"{chunk.get('text', '')}"
            )
        return "\n\n".join(context_parts)

    def _format_sources(self, chunks: List[Dict]) -> List[Dict]:
        sources = []
        seen = set()

        for chunk in chunks:
            doc_id = chunk.get("doc_id")
            if doc_id and doc_id not in seen:
                sources.append({
                    "doc_id": doc_id,
                    "filename": chunk.get("filename", "Unknown"),
                    "chunk_index": chunk.get("chunk_index", 0)
                })
                seen.add(doc_id)

        return sources

    def _generate_answer(self, question: str, context: str) -> str:
        prompt = f"""
        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        result = self.generator(
            prompt,
            max_length=256,
            do_sample=False
        )

        return result[0]["generated_text"].strip()
