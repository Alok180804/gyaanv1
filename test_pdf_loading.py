#!/usr/bin/env python3
"""
Test PDF Loading
"""

from config import FOLDER_ID
from document_loader import DocumentLoader

print("Loading documents with PDF support...\n")
try:
    documents = DocumentLoader(FOLDER_ID).load_all_documents()
    
    print(f"Total documents loaded: {len(documents)}\n")
    
    # Group by type
    by_type = {}
    for doc in documents:
        doc_type = doc['metadata']['file_type']
        by_type[doc_type] = by_type.get(doc_type, 0) + 1
    
    print("By Type:")
    for doc_type, count in sorted(by_type.items()):
        print(f"  • {doc_type}: {count}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
