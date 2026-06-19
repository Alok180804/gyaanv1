#!/usr/bin/env python3
"""
Interactive Query Tester
Test your RAG system with custom queries
"""

from config import COLLECTION_NAME
from local_embedder import LocalEmbedder
from qdrant_manager import QdrantManager


def search_documents(query, top_k=5):
    """Search documents with a query"""
    try:
        embedder = LocalEmbedder()
        qdrant = QdrantManager()
        
        print(f"\n🔍 Searching for: \"{query}\"\n")
        
        # Convert query to vector
        query_vector = embedder.embed_query(query)
        
        # Search
        results = qdrant.search(
            COLLECTION_NAME,
            query_vector,
            limit=top_k
        )
        
        if not results:
            print("❌ No results found")
            return
        
        print(f"✅ Found {len(results)} results:\n")
        
        for idx, result in enumerate(results, 1):
            score = result.score
            content = result.payload.get('content', '')
            file_name = result.payload.get('file_name', 'Unknown')
            file_type = result.payload.get('file_type', 'Unknown')
            
            # Format score indicator
            score_indicator = '✅' if score > 0.7 else '⚠️ ' if score > 0.5 else '❌'
            
            print("=" * 80)
            print(f"RESULT {idx} {score_indicator}")
            print("=" * 80)
            print(f"Similarity: {score:.4f}")
            print(f"File: {file_name}")
            print(f"Type: {file_type}")
            
            # Show more metadata if available
            if "slide_number" in result.payload:
                print(f"Slide #: {result.payload['slide_number']}")
            if "sheet_name" in result.payload:
                print(f"Sheet: {result.payload['sheet_name']}")
            if "chunk_number" in result.payload:
                print(f"Chunk #: {result.payload['chunk_number']}")
            
            print(f"\nContent ({len(content)} chars):")
            print("-" * 80)
            # Show first 500 characters
            preview = content[:500] if len(content) > 500 else content
            print(preview)
            if len(content) > 500:
                print(f"\n... ({len(content) - 500} more characters)")
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Interactive query tester"""
    print("\n" + "=" * 80)
    print("  RAG SYSTEM - INTERACTIVE QUERY TESTER")
    print("=" * 80)
    print("\nYou can now test your RAG system with any query!")
    print("Type 'exit' or 'quit' to stop\n")
    
    while True:
        try:
            query = input("📌 Enter your query: ").strip()
            
            if not query:
                print("⚠️  Please enter a query")
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Allow optional top_k parameter: "query | 10" for 10 results
            top_k = 5
            if '|' in query:
                query, top_k_str = query.rsplit('|', 1)
                try:
                    top_k = int(top_k_str.strip())
                except ValueError:
                    pass
            
            search_documents(query, top_k)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
