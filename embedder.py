from google import genai


class Embedder:

    def __init__(self, api_key):

        self.client = genai.Client(
            api_key=api_key
        )

    def embed_chunks(
        self,
        chunks
    ):

        embedded_chunks = []

        total = len(chunks)

        for idx, chunk in enumerate(
            chunks,
            start=1
        ):

            print(
                f"Embedding {idx}/{total}",
                end="\r"
            )

            response = (
                self.client.models.embed_content(
                    model="gemini-embedding-2",
                    contents=chunk["content"]
                )
            )

            vector = (
                response.embeddings[0]
                .values
            )

            embedded_chunks.append(
                {
                    "content":
                    chunk["content"],

                    "metadata":
                    chunk["metadata"],

                    "embedding":
                    vector
                }
            )

        print()

        return embedded_chunks

    def embed_query(
        self,
        query
    ):

        response = (
            self.client.models.embed_content(
                model="gemini-embedding-2",
                contents=query
            )
        )

        return (
            response.embeddings[0]
            .values
        )