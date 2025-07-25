from fastapi import FastAPI, UploadFile,Query, File
from .ingestion import parse_pdf
from .embedding import build_faiss_index
from .search import search_chunks
from .llm import get_reasoning_response
from .rag import run_rag

import os


app = FastAPI()

UPLOAD_DIR = "app/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        chunks = parse_pdf(file_path)
        return {"filename": file.filename, "chunks": chunks}
    
    return {"error": "Only PDF supported right now."}


@app.post("/embed")
async def embed_document(filename: str = Query(...)):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        return {"error": "File not found"}

    chunks = parse_pdf(path)
    result = build_faiss_index(chunks, filename)
    return {"status": result}

@app.post("/search")
def search(query: str = Query(...), filename: str = Query(...)):
    return search_chunks(query, filename)

@app.post("/reason")
def reason(query: str = Query(...), filename: str = Query(...)):
    # Reuse existing logic
    top_k = 5
    search_output = search_chunks(query, filename, k=top_k)

    if "results" not in search_output:
        return {"error": "Search failed"}

    top_chunks = [r["chunk"] for r in search_output["results"]]
    llm_response = get_reasoning_response(query, top_chunks)

    try:
        # Try parsing response to JSON
        import json
        return json.loads(llm_response)
    except:
        # If parsing fails, return raw
        return {"raw_response": llm_response}


@app.post("/reason")
async def reason(query: str = Query(...), filename: str = Query(...)):
    result = run_rag(query, filename)
    return result
