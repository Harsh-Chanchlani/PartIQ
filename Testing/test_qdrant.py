from qdrant_client import QdrantClient

print("Starting Qdrant connection test...", flush=True)

try:
    client = QdrantClient(
        url="http://localhost:6333",
        timeout=10
    )

    print("Client initialized!", flush=True)

    collections = client.get_collections()

    print("Connection successful!", flush=True)
    print("Collections:", collections, flush=True)

except Exception as e:
    print("Error connecting to Qdrant:", repr(e), flush=True)