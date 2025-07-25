import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_reasoning_response(query: str, context_chunks: list):
    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""
You are a reasoning engine that analyzes natural-language queries and responds based on provided documents.

Instructions:
- Understand the user query.
- Use the document excerpts provided to find relevant information.
- Based on that, return a structured decision.

Respond in this JSON format:
{{
  "decision": "approved | rejected | unknown",
  "amount": <number or null>,
  "justification": "Detailed explanation referring to specific parts of the document"
}}

Query:
{query}

Document Excerpts:
{context}

If the query is not answerable using the excerpts, say "unknown" in decision and explain why.
"""
    
    response = model.generate_content(prompt)
    return response.text
