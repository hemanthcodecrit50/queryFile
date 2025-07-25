import cohere
import faiss
import numpy as np
import os
import pickle
from .llm import get_reasoning_response

co = cohere.Client(os.getenv("COHERE_API_KEY"))

DATA_DIR = "app/data"

def get_query_embedding(query: str):
    response = co.embed(texts=[query], model="embed-english-v3.0", input_type="search_query")
    return response.embeddings[0]

def retrieve_relevant_chunks(query: str, filename: str, top_k=5):
    # Load FAISS index
    index_path = os.path.join(DATA_DIR, f"{filename}.index")
    chunks_path = os.path.join(DATA_DIR, f"{filename}.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return None, "FAISS index or chunk file missing."

    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    # Embed the query
    query_vec = np.array(get_query_embedding(query)).astype('float32').reshape(1, -1)

    # Search
    distances, indices = index.search(query_vec, top_k)
    selected_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]

    return selected_chunks, None

def run_rag(query: str, filename: str):
    chunks, error = retrieve_relevant_chunks(query, filename)
    if error:
        return {"error": error}

    reasoning = get_reasoning_response(query, chunks)
    print("[DEBUG] Raw LLM output:", repr(reasoning))
    import json
    try:
        parsed = json.loads(reasoning)
        return parsed
    except Exception:
        # fallback: return a friendly message
        return {
            "decision": "unknown",
            "justification": "Could not parse a clear answer from the model. Please rephrase your question or check your document."
        }
