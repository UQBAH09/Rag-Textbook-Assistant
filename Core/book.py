import faiss
import numpy as np

from Core.ingestion import ingest_book
from Core.embeddings import build_embedded_chunks, embed_text
from Core.retrieval import retrieve_chunks
from Core.prompts import build_context, build_qa_prompt
from llm.gemini_client import generate_text


class Book:
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.chunks = []
        self.index = None
        self._is_built = False

        # Auto-build on creation
        self._build()

    def _build(self):
        """Build the knowledge base (internal)."""
        structuredBook = ingest_book(self.path)
        self.chunks = build_embedded_chunks(structuredBook)

        vectors = np.array(
            [chunk["embedding"] for chunk in self.chunks],
            dtype="float32"
        )

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

        self._is_built = True

    def _retrieve(self, query: str, k: int = 5):
        """Retrieve relevant chunks (internal)."""
        if not self._is_built:
            raise RuntimeError("Book is not built")

        queryEmbedding = embed_text(query)

        return retrieve_chunks(
            query,
            queryEmbedding,
            self.index,
            self.chunks,
            k
        )

    def ask(self, query: str, k: int = 5, debug_mode: bool = False) -> str:
        """
        Public API: ask a question about the book.
        """
        retrieved_chunks = self._retrieve(query, k)
        context = build_context(retrieved_chunks)
        prompt = build_qa_prompt(query, context)
        
        if debug_mode:
            print(f"Prompt: \n{prompt}")        

        return generate_text(prompt)
