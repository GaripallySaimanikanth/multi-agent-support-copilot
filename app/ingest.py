"""
Usage:
    python -m app.ingest  # ingests all files from data/docs into Chroma
"""
from pathlib import Path
from typing import List
import re

from .config import DOCS_DIR
from .retriever import ChromaRetriever

# Simple loaders for txt/markdown; you can extend for PDF, etc.
TEXT_EXTS = {".txt", ".md", ".markdown"}

def read_text_files(root: Path) -> List[Path]:
    if not root.exists():
        return []
    paths = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_EXTS:
            paths.append(p)
    return paths

def split_into_chunks(text: str, chunk_size: int = 800, chunk_overlap: int = 120) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = end - chunk_overlap
        if start < 0:
            start = 0
    return chunks

def main():
    retriever = ChromaRetriever()
    files = read_text_files(DOCS_DIR)
    if not files:
        print(f"No documents found in {DOCS_DIR}. Add .txt/.md files and re-run.")
        return

    ids, texts, metas = [], [], []
    counter = 0
    for f in files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        for i, chunk in enumerate(split_into_chunks(content)):
            ids.append(f"{f.stem}_{i}")
            texts.append(chunk)
            metas.append({"path": str(f.relative_to(DOCS_DIR)), "chunk": i})
            counter += 1

    retriever.add_texts(texts=texts, metadatas=metas, ids=ids)
    print(f"Ingested {counter} chunks from {len(files)} files into ChromaDB at {retriever.client._db._base_path}")

if __name__ == "__main__":
    main()
