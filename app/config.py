from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = DATA_DIR / "docs"
DB_DIR = DATA_DIR / "chroma"

# Embedding model
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval settings
CHROMA_COLLECTION = "knowledge_base"
TOP_K = 4

# API settings
API_TITLE = "Multi-Agent Support Copilot"
