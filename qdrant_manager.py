from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


class QdrantManager:

    def __init__(self):

        self.client = QdrantClient(
            path="./qdrant_data"
        )

    def create_collection(
        self,
        collection_name,
        vector_size
    ):

        collections = (
            self.client.get_collections()
        )

        collection_names = [
            c.name
            for c in collections.collections
        ]

        if collection_name in collection_names:

            print(
                f"{collection_name} already exists"
            )

            return

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(
            f"{collection_name} created"
        )

    def insert_points(
        self,
        collection_name,
        embedded_chunks
    ):

        points = []

        for idx, chunk in enumerate(
            embedded_chunks
        ):

            payload = {
                **chunk["metadata"],
                "content":
                chunk["content"]
            }

            points.append(
                PointStruct(
                    id=idx,
                    vector=chunk["embedding"],
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points
        )

        print(
            f"Inserted {len(points)} vectors"
        )

    def search(
        self,
        collection_name,
        query_vector,
        limit=5
    ):

        results = (
            self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=limit
            )
        )

        return results.points

    def list_collections(self):

        collections = (
            self.client.get_collections()
        )

        for collection in (
            collections.collections
        ):

            print(
                collection.name
            )