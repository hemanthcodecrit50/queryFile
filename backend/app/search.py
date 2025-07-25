import faiss
import pickle
import numpy as np
from .embedding import get_embeddings
import os

DATA_DIR = "app/data"

def search_chunks(query: str, filename: str, k: int = 5):
    index_path = os.path.join(DATA_DIR, f"{filename}.index")
    chunk_path = os.path.join(DATA_DIR, f"{filename}.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        return {"error": "Index or chunk file not found for this document."}

    # Load FAISS index
    index = faiss.read_index(index_path)

    # Load chunks
    with open(chunk_path, "rb") as f:
        chunks = pickle.load(f)

    # Get embedding for the query
    query_vector = get_embeddings([query])[0]
    query_vector = np.array([query_vector]).astype("float32")

    # Search FAISS
    D, I = index.search(query_vector, k)

    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(chunks):
            results.append({
                "chunk": chunks[idx],
                "score": float(score)
            })
    
    return {"results": results}
