#!/usr/bin/env python3
"""
List All Documents
Shows all documents loaded from Google Drive
"""

from config import FOLDER_ID
from document_loader import DocumentLoader


def list_all_documents():
    """List all documents with details"""
    
    print("\n" + "=" * 100)
    print("  ALL DOCUMENTS IN YOUR GOOGLE DRIVE FOLDER")
    print("=" * 100 + "\n")
    
    try:
        # Load documents
        print("Loading documents from Google Drive...\n")
        loader = DocumentLoader(FOLDER_ID)
        documents = loader.load_all_documents()
        
        print(f"✅ Found {len(documents)} documents\n")
        print("=" * 100)
        
        # Group by type
        docs_by_type = {}
        for doc in documents:
            doc_type = doc['metadata']['file_type']
            if doc_type not in docs_by_type:
                docs_by_type[doc_type] = []
            docs_by_type[doc_type].append(doc)
        
        # Display by type
        for doc_type in sorted(docs_by_type.keys()):
            docs = docs_by_type[doc_type]
            print(f"\n📁 {doc_type.upper()} ({len(docs)} documents)")
            print("-" * 100)
            
            for idx, doc in enumerate(docs, 1):
                meta = doc['metadata']
                file_name = meta.get('file_name', 'Unknown')
                modified_time = meta.get('modified_time', 'Unknown')
                content = doc.get('content', '')
                content_length = len(content)
                
                # Additional info based on type
                extra_info = ""
                if doc_type == "google_slide":
                    extra_info = f" [Slide #{meta.get('slide_number', '?')}]"
                elif doc_type == "google_sheet":
                    extra_info = f" [Sheet: {meta.get('sheet_name', '?')}]"
                
                print(f"\n{idx}. {file_name}{extra_info}")
                print(f"   ID: {meta.get('file_id', 'N/A')}")
                print(f"   Modified: {modified_time}")
                print(f"   Content Length: {content_length:,} characters")
                print(f"   Preview: {content[:200]}...")
        
        # Summary statistics
        print("\n" + "=" * 100)
        print("  SUMMARY STATISTICS")
        print("=" * 100)
        
        total_chars = sum(len(d['content']) for d in documents)
        total_files = {}
        
        for doc in documents:
            file_name = doc['metadata']['file_name']
            total_files[file_name] = total_files.get(file_name, 0) + 1
        
        print(f"\n📊 Total Documents: {len(documents)}")
        print(f"📊 Total Characters: {total_chars:,}")
        print(f"📊 Average per Document: {total_chars // len(documents):,}")
        print(f"📊 Unique Files: {len(total_files)}")
        print(f"📊 By Type:")
        for doc_type, docs in sorted(docs_by_type.items()):
            print(f"   • {doc_type}: {len(docs)}")
        
        print(f"\n📊 Breakdown by File:")
        for file_name in sorted(total_files.keys()):
            count = total_files[file_name]
            file_docs = [d for d in documents if d['metadata']['file_name'] == file_name]
            file_chars = sum(len(d['content']) for d in file_docs)
            print(f"   • {file_name}: {count} documents, {file_chars:,} characters")
        
        print("\n" + "=" * 100 + "\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    list_all_documents()
