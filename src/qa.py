import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline


class QAChatbot:
    def __init__(self):
        # Load embedding model for semantic search
        print("🔹 Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load FAISS index and metadata
        print("🔹 Loading FAISS index and metadata...")
        self.index = faiss.read_index("data/faiss.index")
        self.meta = pickle.load(open("data/metadata.pkl", "rb"))

        # Load Hugging Face model for answer generation
        print("🔹 Loading local language model (flan-t5-base)...")
        self.generator = pipeline("text2text-generation", model="google/flan-t5-base")

    def search(self, query, k=4):
        """Find top-k relevant documents from FAISS index"""
        q_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_emb.astype("float32"), k)
        return [self.meta[i] for i in I[0]]

    def ask(self, question):
        """Answer a question using context from top documents"""
        print("🔹 Searching for relevant context...")
        results = self.search(question)
        context = "\n\n".join(
            [f"{r['title']} - {r['url']}\n{r.get('text', '')}" for r in results]
        )

        prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question: {question}
Answer:
"""

        print("🔹 Generating answer...")
        output = self.generator(prompt, max_length=300, temperature=0.0)
        answer = output[0]["generated_text"].strip()

        return answer, results
