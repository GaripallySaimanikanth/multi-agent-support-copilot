🚀 Multi-Agent Support Copilot
An AI-powered support assistant built with FastAPI, LangChain, LangGraph, ChromaDB, and Google Vertex AI (Gemini).
It uses a multi-agent architecture (Retriever → Reasoner → Responder) to answer customer questions with grounded, document-backed responses.
✨ Features
Retriever Agent – Finds relevant documents using embeddings + ChromaDB
Reasoner Agent – Summarizes and synthesizes context from retrieved docs
Responder Agent – Generates a final, cited response using Gemini 1.5 Flash
📚 RAG pipeline with local persistence for knowledge base
 FastAPI backend with /ask endpoint for queries
🛠️ Tech Stack
Python 3.10+
FastAPI
Uvicorn
LangChain + LangGraph
ChromaDB (vector store)
Google Vertex AI (Gemini + Embeddings)

-d '{"question": "How do I request a refund?"}'

Example Response
{
  "answer": "You can request a refund by contacting support via the portal.",

📂 Project Structure
multi-agent-support-copilot/
├── app/
│   ├── api.py        # FastAPI routes
│   ├── agents.py     # Multi-agent workflow
│   ├── retriever.py  # Chroma retriever
│   ├── ingest.py     # Ingest + index documents
│   └── config.py     # Configs & env vars
├── data/             # Input documents
├── .chroma_db/       # Local vector store
├── requirements.txt
├── README.md
└── .env
🔧 Development Notes



