#!/usr/bin/env python3
"""
Complete RAG Pipeline Test Script
Tests: Load → Chunk → Embed → Store → Search
"""

from config import (
    FOLDER_ID,
    GOOGLE_API_KEY,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from document_loader import DocumentLoader
from chunker import Chunker
from embedder import Embedder
from qdrant_manager import QdrantManager


def print_section(title):
    """Print a nice section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def test_pipeline():
    """Run the complete pipeline"""
    
    # ============================================
    # STEP 1: LOAD DOCUMENTS
    # ============================================
    print_section("STEP 1: LOADING DOCUMENTS FROM GOOGLE DRIVE")
    
    try:
        loader = DocumentLoader(FOLDER_ID)
        documents = loader.load_all_documents()
        print(f"✅ Loaded {len(documents)} documents")
        
        if documents:
            print(f"\nSample document:")
            print(f"  File: {documents[0]['metadata']['file_name']}")
            print(f"  Type: {documents[0]['metadata']['file_type']}")
            print(f"  Content: {documents[0]['content'][:200]}...")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return
    
    # ============================================
    # STEP 2: CHUNK DOCUMENTS
    # ============================================
    print_section("STEP 2: CHUNKING DOCUMENTS")
    
    try:
        chunker = Chunker(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = chunker.chunk_documents(documents)
        print(f"✅ Created {len(chunks)} chunks")
        
        if chunks:
            print(f"\nSample chunk:")
            print(f"  Chunk #: {chunks[0]['metadata'].get('chunk_number', 'N/A')}")
            print(f"  File: {chunks[0]['metadata']['file_name']}")
            print(f"  Content: {chunks[0]['content'][:200]}...")
    except Exception as e:
        print(f"❌ Error chunking documents: {e}")
        return
    
    # ============================================
    # STEP 3: EMBED CHUNKS
    # ============================================
    print_section("STEP 3: EMBEDDING CHUNKS (Using Gemini API)")
    
    try:
        embedder = Embedder(GOOGLE_API_KEY)
        
        # Limit to first 10 chunks for testing (to save API calls & time)
        chunks_to_embed = chunks[:10]
        print(f"Embedding {len(chunks_to_embed)} chunks (limited for testing)...\n")
        
        embedded_chunks = embedder.embed_chunks(chunks_to_embed)
        print(f"\n✅ Embedded {len(embedded_chunks)} chunks")
        
        if embedded_chunks:
            embedding = embedded_chunks[0]['embedding']
            print(f"\nSample embedding:")
            print(f"  Vector size: {len(embedding)} dimensions")
            print(f"  First 10 values: {embedding[:10]}")
    except Exception as e:
        print(f"❌ Error embedding chunks: {e}")
        return
    
    # ============================================
    # STEP 4: STORE IN QDRANT
    # ============================================
    print_section("STEP 4: STORING IN QDRANT DATABASE")
    
    try:
        qdrant = QdrantManager()
        vector_size = len(embedded_chunks[0]['embedding'])
        
        qdrant.create_collection(COLLECTION_NAME, vector_size)
        qdrant.insert_points(COLLECTION_NAME, embedded_chunks)
        
        print(f"✅ Created collection: {COLLECTION_NAME}")
        print(f"✅ Inserted {len(embedded_chunks)} vectors")
        print(f"✅ Vector database stored at: ./qdrant_data/")
    except Exception as e:
        print(f"❌ Error storing in Qdrant: {e}")
        return
    
    # ============================================
    # STEP 5: SEARCH WITH QUERIES
    # ============================================
    print_section("STEP 5: TESTING SEARCH WITH QUERIES")
    
    # Test queries
    test_queries = [
        "What is the main topic of the documents?",
        "Tell me about the key points",
        "Summarize the important information"
    ]
    
    try:
        for query_idx, query in enumerate(test_queries, 1):
            print(f"\n📌 Query {query_idx}: \"{query}\"\n")
            
            # Convert query to vector
            query_vector = embedder.embed_query(query)
            print(f"   Query vector size: {len(query_vector)} dimensions")
            
            # Search
            results = qdrant.search(
                COLLECTION_NAME,
                query_vector,
                limit=3
            )
            
            print(f"   Found {len(results)} results:\n")
            
            # Display results
            for result_idx, result in enumerate(results, 1):
                score = result.score
                content = result.payload.get('content', '')[:300]
                file_name = result.payload.get('file_name', 'Unknown')
                
                print(f"   Result {result_idx}:")
                print(f"   ├─ Similarity Score: {score:.4f} {'✅' if score > 0.7 else '⚠️'}")
                print(f"   ├─ File: {file_name}")
                print(f"   └─ Content: {content}...\n")
    
    except Exception as e:
        print(f"❌ Error searching: {e}")
        return
    
    # ============================================
    # SUMMARY
    # ============================================
    print_section("✅ TEST COMPLETE")
    print(f"""
Summary:
  • Documents loaded: {len(documents)}
  • Chunks created: {len(chunks)}
  • Chunks embedded: {len(embedded_chunks)}
  • Vector database: ./qdrant_data/
  • Collection name: {COLLECTION_NAME}
  
Next steps:
  1. Run test_query.py again to test more queries
  2. Modify test_queries in this script to test custom queries
  3. Run the full pipeline without limiting chunks
  4. Integrate with your LLM (ChatGPT, Claude, etc.)
    """)


if __name__ == "__main__":
    try:
        test_pipeline()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
