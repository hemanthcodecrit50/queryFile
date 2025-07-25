
import cohere
import faiss
import numpy as np
import pickle
import os


co = cohere.Client(os.getenv("COHERE_API_KEY"))

def get_embeddings(texts, model="embed-english-v3.0"):
    response = co.embed(texts=texts, model=model, input_type="search_document")
    return response.embeddings

def build_faiss_index(chunks, filename):
    vectors = get_embeddings(chunks)
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype('float32'))

    # Save index + chunks
    faiss.write_index(index, f"app/data/{filename}.index")
    with open(f"app/data/{filename}.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return f"{len(chunks)} chunks indexed using Cohere."
