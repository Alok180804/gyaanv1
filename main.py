from config import FOLDER_ID

from document_loader import (
    DocumentLoader
)

from chunker import Chunker


def main():

    documents = (
        DocumentLoader(
            FOLDER_ID
        ).load_all_documents()
    )

    chunks = (
        Chunker(
            chunk_size=1000,
            chunk_overlap=200
        ).chunk_documents(
            documents
        )
    )

    print(
        f"\nDocuments: {len(documents)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print("\nSample Metadata:\n")

    print(
        chunks[0]["metadata"]
    )

    print("\nSample Chunk:\n")

    print(
        chunks[0]["content"]
    )


if __name__ == "__main__":
    main()
