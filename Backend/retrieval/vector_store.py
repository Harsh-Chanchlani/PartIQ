from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333"
)

from qdrant_client.models import (
    Distance,
    VectorParams
)

COLLECTION = "component_documents"


def create_collection(vector_size):

    if not client.collection_exists(COLLECTION):

        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

from qdrant_client.models import PointStruct
from uuid import uuid5, NAMESPACE_URL


def store_chunks(chunks, embeddings, document_id):

    points = []

    for index, chunk in enumerate(chunks):

        point_id = str(uuid5(
            NAMESPACE_URL,
            f"{document_id}:{index}"
        ))

        points.append(
            PointStruct(
                id=point_id,

                vector=embeddings[index].tolist(),

                payload={
                    "document_id": document_id,
                    "filename": chunk["filename"],
                    "page": chunk["page"],
                    "chunk_index": index,
                    "text": chunk["text"],
                    "component": chunk.get("component"),
                    "manufacturer": chunk.get("manufacturer")
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )