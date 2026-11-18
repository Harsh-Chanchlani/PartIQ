from sentence_transformers import (
    SentenceTransformer
)

import numpy as np


class Embedder:

    def __init__(self, device="cpu"):

        self.model = SentenceTransformer(
            "BAAI/bge-m3",
            device=device,
            local_files_only=True
        )

    def generate_embeddings(self, texts):

        vectors = self.model.encode(
            texts,
            batch_size=8,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return vectors