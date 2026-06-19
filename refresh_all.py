#!/usr/bin/env python3
"""
Complete Refresh Pipeline
Loads everything (including PDFs), chunks, embeds, and stores in Qdrant
"""

import shutil
import os
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


def print_header(title):
    """Print section header"""
    print("\n" + "=" * 100)
    print(f"  {title}")
    print("=" * 100 + "\n")


def delete_old_database():
    """Delete old Qdrant database"""
    print_header("STEP 0: CLEARING OLD DATABASE")
    
    db_path = "./qdrant_data"
    if os.path.exists(db_path):
        print(f"Deleting old database at {db_path}...")
        try:
            shutil.rmtree(db_path)
            print("✅ Old database deleted\n")
        except Exception as e:
            print(f"⚠️  Could not delete old database: {e}")
            print("Continuing anyway...\n")
    else:
        print("✅ No old database found\n")


def load_documents():
    """Load all documents including PDFs"""
    print_header("STEP 1: LOADING ALL DOCUMENTS (INCLUDING PDFs)")
    
    try:
        loader = DocumentLoader(FOLDER_ID)
        documents = loader.load_all_documents()
        
        print(f"✅ Loaded {len(documents)} documents\n")
        
        # Show breakdown
        by_type = {}
        for doc in documents:
            doc_type = doc['metadata']['file_type']
            by_type[doc_type] = by_type.get(doc_type, 0) + 1
        
        print("Breakdown by type:")
        for doc_type, count in sorted(by_type.items()):
            print(f"  • {doc_type}: {count}")
        
        total_chars = sum(len(d['content']) for d in documents)
        print(f"\nTotal characters: {total_chars:,}")
        
        return documents
    
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        import traceback
        traceback.print_exc()
        return None


def chunk_documents(documents):
    """Chunk all documents"""
    print_header("STEP 2: CHUNKING DOCUMENTS")
    
    try:
        chunker = Chunker(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = chunker.chunk_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks")
        print(f"  Chunk size: {CHUNK_SIZE} characters")
        print(f"  Overlap: {CHUNK_OVERLAP} characters\n")
        
        total_chars = sum(len(c['content']) for c in chunks)
        print(f"Total chunk characters: {total_chars:,}")
        
        return chunks
    
    except Exception as e:
        print(f"❌ Error chunking documents: {e}")
        import traceback
        traceback.print_exc()
        return None


def embed_chunks(chunks):
    """Embed all chunks"""
    print_header("STEP 3: EMBEDDING ALL CHUNKS (Using Gemini API)")
    
    try:
        embedder = Embedder(GOOGLE_API_KEY)
        
        print(f"Embedding {len(chunks)} chunks...\n")
        print("(This may take several minutes depending on chunk count)\n")
        
        embedded_chunks = embedder.embed_chunks(chunks)
        
        print(f"\n✅ Embedded {len(embedded_chunks)} chunks")
        
        if embedded_chunks:
            vector_size = len(embedded_chunks[0]['embedding'])
            print(f"Vector size: {vector_size} dimensions\n")
        
        return embedded_chunks
    
    except Exception as e:
        print(f"❌ Error embedding chunks: {e}")
        import traceback
        traceback.print_exc()
        return None


def store_in_qdrant(embedded_chunks):
    """Store embedded chunks in Qdrant"""
    print_header("STEP 4: STORING IN QDRANT DATABASE")
    
    try:
        qdrant = QdrantManager()
        
        if not embedded_chunks:
            print("❌ No chunks to store")
            return False
        
        vector_size = len(embedded_chunks[0]['embedding'])
        
        print(f"Creating collection '{COLLECTION_NAME}'...")
        qdrant.create_collection(COLLECTION_NAME, vector_size)
        
        print(f"Inserting {len(embedded_chunks)} vectors...")
        qdrant.insert_points(COLLECTION_NAME, embedded_chunks)
        
        print(f"\n✅ Successfully stored in Qdrant")
        print(f"  Database: ./qdrant_data/")
        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Total vectors: {len(embedded_chunks)}\n")
        
        return True
    
    except Exception as e:
        print(f"❌ Error storing in Qdrant: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_search(embedded_chunks):
    """Test the system with a sample search"""
    print_header("STEP 5: TESTING SEARCH")
    
    try:
        embedder = Embedder(GOOGLE_API_KEY)
        qdrant = QdrantManager()
        
        test_query = "travel pdf content"
        print(f"Test query: \"{test_query}\"\n")
        
        query_vector = embedder.embed_query(test_query)
        results = qdrant.search(COLLECTION_NAME, query_vector, limit=3)
        
        if results:
            print(f"✅ Found {len(results)} results:\n")
            for idx, result in enumerate(results, 1):
                print(f"Result {idx}: {result.score:.4f} - {result.payload.get('file_name', 'Unknown')}")
            print()
        else:
            print("⚠️  No results found (this is normal if database is small)\n")
        
        return True
    
    except Exception as e:
        print(f"⚠️  Error testing search: {e}")
        return True  # Don't fail the whole process


def main():
    """Run complete refresh pipeline"""
    
    print("\n" + "=" * 100)
    print("  COMPLETE RAG REFRESH - LOADING ALL DOCUMENTS + PDFs")
    print("=" * 100)
    
    # Step 0: Delete old database
    delete_old_database()
    
    # Step 1: Load documents
    documents = load_documents()
    if not documents:
        return False
    
    # Step 2: Chunk documents
    chunks = chunk_documents(documents)
    if not chunks:
        return False
    
    # Step 3: Embed chunks
    embedded_chunks = embed_chunks(chunks)
    if not embedded_chunks:
        return False
    
    # Step 4: Store in Qdrant
    success = store_in_qdrant(embedded_chunks)
    if not success:
        return False
    
    # Step 5: Test search
    test_search(embedded_chunks)
    
    # Summary
    print_header("✅ REFRESH COMPLETE")
    print(f"""
Summary:
  ✓ Documents loaded: {len(documents)}
  ✓ Chunks created: {len(chunks)}
  ✓ Vectors embedded: {len(embedded_chunks)}
  ✓ Stored in Qdrant: ./qdrant_data/

Next Steps:
  1. Test with interactive search:
     python3 interactive_search.py
  
  2. Search your documents including PDFs:
     Try queries about your PDF content!
  
  3. All documents are now indexed and searchable
  """)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Refresh failed. Please check the errors above.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Refresh interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
