import os
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load scraped pages
with open("data/pages.jsonl", "r", encoding="utf-8") as f:
    docs = [json.loads(line) for line in f]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [d["text"] for d in docs]
print(f"Encoding {len(texts)} chunks...")

# Generate embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Create FAISS index
faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
faiss_index.add(np.array(embeddings))

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Save index and metadata
faiss.write_index(faiss_index, "data/faiss.index")
with open("data/metadata.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ Saved embeddings to data/faiss.index and data/metadata.pkl")
