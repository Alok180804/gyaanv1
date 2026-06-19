#!/usr/bin/env python3
"""
Local Embedder - No API needed!
Uses sentence-transformers for free, offline embeddings
"""

from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """Local embeddings using sentence-transformers"""

    def __init__(self):
        """Load the model (downloads on first run)"""
        print("Loading local embedding model...")
        print("(First time run downloads ~30MB model)\n")
        
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded!\n")

    def embed_chunks(self, chunks):
        """Embed all chunks"""
        embedded_chunks = []
        total = len(chunks)

        for idx, chunk in enumerate(chunks, start=1):
            print(f"Embedding {idx}/{total}", end="\r")

            # Local embedding (no API call)
            vector = self.model.encode(chunk["content"])

            embedded_chunks.append({
                "content": chunk["content"],
                "metadata": chunk["metadata"],
                "embedding": vector.tolist()  # Convert numpy to list
            })

        print()
        return embedded_chunks

    def embed_query(self, query):
        """Embed a query"""
        return self.model.encode(query).tolist()
