from Backend.Ingestion.embedder import Embedder

embedder = Embedder(device="cpu")

texts = [
    "ESP32 supports Wi-Fi connectivity",
    "ESP32 has a 3.3V supply requirement",
    "STM32 is a microcontroller family"
    ]

vectors = embedder.generate_embeddings(
    texts
)

print(vectors.shape)