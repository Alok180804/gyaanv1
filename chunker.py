# chunker.py

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


class Chunker:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False,
            )
        )

    def chunk_documents(
        self,
        documents
    ):

        chunks = []

        for doc in documents:

            content = doc.get(
                "content",
                ""
            )

            if not content.strip():
                continue

            split_chunks = (
                self.splitter.split_text(
                    content
                )
            )

            for idx, chunk in enumerate(
                split_chunks
            ):

                chunks.append(
                    {
                        "content": chunk,
                        "metadata": {
                            **doc["metadata"],
                            "chunk_number": idx
                        }
                    }
                )

        return chunks