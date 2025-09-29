"""
Very light local eval:
- Provide a list of (question, should_contain) pairs
- We check if the final answer contains the expected phrase(s)
"""
from typing import List, Tuple
from .retriever import ChromaRetriever
from .agents import SupportCopilot

TESTS: List[Tuple[str, str]] = [
    ("What is this project about?", "support copilot"),
    ("Which vector database is used?", "Chroma"),
]

def run_eval() -> None:
    copilot = SupportCopilot(ChromaRetriever())
    passed, total = 0, len(TESTS)
    for q, expected in TESTS:
        res = copilot.ask(q).answer.lower()
        ok = expected.lower() in res
        print(f"Q: {q}\n✓ expected '{expected}' -> {'PASS' if ok else 'FAIL'}\n")
        passed += int(ok)
    print(f"Score: {passed}/{total}")

if __name__ == "__main__":
    run_eval()
