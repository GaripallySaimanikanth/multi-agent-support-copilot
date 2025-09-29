import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Dict, Any, Optional

from .config import DB_DIR, CHROMA_COLLECTION, EMBED_MODEL_NAME, TOP_K

class ChromaRetriever:
    def __init__(self, persist_dir: Path = DB_DIR, collection_name: str = CHROMA_COLLECTION):
        persist_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(persist_dir), settings=Settings(allow_reset=False)
        )
        self.embedding_fn = embedding_functions.S
