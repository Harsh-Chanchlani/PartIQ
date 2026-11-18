import sys
import os

# Allow imports like "from Backend.Ingestion.xxx import yyy"
# by making the project root visible to Python's module finder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Backend.Ingestion.pdf_extractor import extract_pdf
from Backend.Ingestion.chunker import chunk_page
from Backend.Ingestion.embedder import Embedder
from Backend.retrieval.vector_store import (
    create_collection,
    store_chunks,
    client,
    COLLECTION,
)

PDF_PATH = "data/uploads/ESP32_Datasheet.pdf"
DOCUMENT_ID = "esp32-datasheet-v1"
VECTOR_SIZE = 1024  # BGE-M3 always outputs 1024-dimensional vectors


# ── STEP 1: Extract ───────────────────────────────────────────────────────────

print("\n[1/5] Extracting PDF...")

pages = extract_pdf(PDF_PATH)

print(f"      → {len(pages)} pages extracted")
assert len(pages) > 0, "No pages extracted — check PDF path or text layer"


# ── STEP 2: Chunk ─────────────────────────────────────────────────────────────

print("\n[2/5] Chunking pages...")

all_chunks = []

for page_data in pages:

    # chunk_page returns plain strings — that is correct for a pure text chunker.
    # HERE is where we attach metadata so vector_store gets the dicts it expects.
    raw_text_chunks = chunk_page(page_data["text"])

    for raw_text in raw_text_chunks:

        all_chunks.append({
            "text": raw_text,
            "page": page_data["page"],
            "filename": os.path.basename(PDF_PATH),
            "component": "ESP32",
            "manufacturer": "Espressif",
        })

print(f"      → {len(all_chunks)} chunks total")
assert len(all_chunks) > 0, "Chunking produced nothing — check chunker logic"


# ── STEP 3: Embed ─────────────────────────────────────────────────────────────

print("\n[3/5] Generating embeddings (may take ~30s on CPU)...")

embedder = Embedder(device="cpu")
texts = [chunk["text"] for chunk in all_chunks]
embeddings = embedder.generate_embeddings(texts)

print(f"      → embeddings shape: {embeddings.shape}")
assert embeddings.shape == (len(all_chunks), VECTOR_SIZE), (
    f"Expected ({len(all_chunks)}, {VECTOR_SIZE}), got {embeddings.shape}"
)


# ── STEP 4: Store ─────────────────────────────────────────────────────────────

print("\n[4/5] Storing in Qdrant...")

create_collection(VECTOR_SIZE)
store_chunks(all_chunks, embeddings, DOCUMENT_ID)

count = client.count(collection_name=COLLECTION).count
print(f"      → {count} points now in '{COLLECTION}'")
assert count > 0, "Qdrant collection is empty after upsert — is Qdrant running?"


# ── STEP 5: Search ────────────────────────────────────────────────────────────

print("\n[5/5] Testing retrieval...")

query_text = "What is the supply voltage of ESP32?"
query_vector = embedder.generate_embeddings([query_text])[0].tolist()

results = client.search(
    collection_name=COLLECTION,
    query_vector=query_vector,
    limit=3,
)

print(f"\n      Query : '{query_text}'")
print(f"      Top {len(results)} results:\n")

for i, result in enumerate(results):
    print(f"      [{i + 1}] score={result.score:.4f}  page={result.payload['page']}")
    print(f"           {result.payload['text'][:200]}")
    print()

assert len(results) > 0, "Search returned nothing"
assert results[0].score > 0.3, f"Top score too low: {results[0].score}"

print("✅  Full pipeline test PASSED\n")

