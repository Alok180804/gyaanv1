#!/usr/bin/env python3
"""
Quick Test - Run immediately to test a single query
"""

from config import COLLECTION_NAME, GOOGLE_API_KEY
from embedder import Embedder
from qdrant_manager import QdrantManager


def quick_test():
    """Quick single query test"""
    
    print("\n" + "=" * 80)
    print("  QUICK TEST - SINGLE QUERY")
    print("=" * 80 + "\n")
    
    # Test query
    query = "What is fashion ecommerce about?"
    print(f"Query: \"{query}\"\n")
    
    try:
        # Initialize
        embedder = Embedder(GOOGLE_API_KEY)
        qdrant = QdrantManager()
        
        # Embed query
        print("Embedding query...")
        query_vector = embedder.embed_query(query)
        print(f"✅ Vector created: {len(query_vector)} dimensions\n")
        
        # Search
        print("Searching database...")
        results = qdrant.search(COLLECTION_NAME, query_vector, limit=5)
        
        if not results:
            print("❌ No results found")
            return
        
        print(f"✅ Found {len(results)} results:\n")
        
        # Show results
        for idx, result in enumerate(results, 1):
            score = result.score
            content = result.payload.get('content', '')[:300]
            file_name = result.payload.get('file_name', 'Unknown')
            
            symbol = '✅' if score > 0.7 else '⚠️'
            
            print(f"Result {idx}: {symbol}")
            print(f"  Score: {score:.4f}")
            print(f"  File: {file_name}")
            print(f"  Text: {content}...\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    quick_test()
