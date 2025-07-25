
from fastapi import FastAPI, UploadFile,Query, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .ingestion import parse_pdf
from .embedding import build_faiss_index
from .search import search_chunks
from .llm import get_reasoning_response
from .rag import run_rag
import os


from dotenv import load_dotenv
load_dotenv()

port = int(os.getenv("PORT", 8000))
host = os.getenv("HOST", "127.0.0.1")

if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    print("[DEBUG] Query:", query)
    print("[DEBUG] Search Output:", search_output)

    if "results" not in search_output:
        print("[DEBUG] Search failed.")
        return {"error": "Search failed"}

    top_chunks = [r["chunk"] for r in search_output["results"]]
    print("[DEBUG] Top Chunks:", top_chunks)

    # Optionally, print the prompt if you build it in get_reasoning_response
    llm_response = get_reasoning_response(query, top_chunks)
    print("[DEBUG] LLM Response:", llm_response)

    try:
        # Try parsing response to JSON
        import json
        parsed = json.loads(llm_response)
        print("[DEBUG] Parsed LLM Response:", parsed)
        return parsed
    except Exception as e:
        print("[DEBUG] LLM Response could not be parsed as JSON:", e)
        return {"raw_response": llm_response}


# @app.post("/reason")
# async def reason(query: str = Query(...), filename: str = Query(...)):
#     result = run_rag(query, filename)
#     return result
