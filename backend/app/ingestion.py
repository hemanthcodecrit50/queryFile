import pdfplumber
from .utils import chunk_text

def parse_pdf(path: str):
    with pdfplumber.open(path) as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    chunks = chunk_text(full_text)
    return chunks
