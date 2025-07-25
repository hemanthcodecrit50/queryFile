from fastapi import FastAPI, UploadFile,Query, File
from .ingestion import parse_pdf
from .embedding import build_faiss_index
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

