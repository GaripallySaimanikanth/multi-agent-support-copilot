"""
FastAPI backend:
- POST /ask { "query": "..." } -> grounded answer + sources
- POST /ingest -> (re)ingest docs from data/docs
Run: uvicorn app.api:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel

from .config import API_TITLE
from .retriever import ChromaRetriever
from .agents import SupportCopilot
from .ingest import main as ingest_main

app = FastAPI(title=API_TITLE)
_retriever = ChromaRetriever()
_copilot = SupportCopilot(_retriever)

class AskReq(BaseModel):
    query: str

@app.post("/ask")
def ask(req: AskReq):
    out = _copilot.ask(req.query)
    return {
        "answer": out.answer,
        "sources": out.sources,
    }

@app.post("/ingest")
def ingest():
    ingest_main()
    return {"status": "ok"}
