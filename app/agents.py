from dataclasses import dataclass
from typing import List, Dict, Any
import textwrap

from .retriever import ChromaRetriever

# --------- Agent Outputs ---------
@dataclass
class RetrievalResult:
    query: str
    contexts: List[Dict[str, Any]]

@dataclass
class ReasoningResult:
    query: str
    rationale: str
    selected_contexts: List[Dict[str, Any]]

@dataclass
class ResponseResult:
    answer: str
    sources: List[Dict[str, Any]]

# --------- Agents ---------
class RetrieverAgent:
    """Finds relevant passages for a user query."""
    def __init__(self, retriever: ChromaRetriever):
        self.retriever = retriever

    def run(self, query: str) -> RetrievalResult:
        contexts = self.retriever.query(query)
        return RetrievalResult(query=query, contexts=contexts)

class ReasonerAgent:
    """
    Lightweight heuristic 'reasoner':
    - ranks contexts by distance if available
    - extracts the most relevant sentences
    """
    def run(self, retrieval: RetrievalResult) -> ReasoningResult:
        ctxs = retrieval.contexts
        # Sort by distance if provided (lower is better)
        ctxs_sorted = sorted(ctxs, key=lambda x: x.get("distance") or 0.0)
        # Keep top 3 and lightly compress (first ~3 sentences)
        selected = []
        for c in ctxs_sorted[:3]:
            snippet = " ".join(c["text"].split())  # normalize spaces
            snippet = " ".join(snippet.split(". ")[:3])  # take first ~3 sentences
            selected.append({**c, "text": snippet})

        rationale = (
            "Selected top passages by semantic similarity and extracted concise snippets "
            "to ground the final answer."
        )
        return ReasoningResult(query=retrieval.query, rationale=rationale, selected_contexts=selected)

class ResponderAgent:
    """Composes a grounded response using the selected contexts."""
    def run(self, reasoning: ReasoningResult) -> ResponseResult:
        context_block = "\n\n".join(
            f"- {c['text']}" for c in reasoning.selected_contexts
        ) or "- (no context retrieved)"

        answer = textwrap.dedent(f"""
        Answer (grounded):
        Based on the retrieved project documentation and notes, here is a concise response
        to your query:

        • {reasoning.query}

        Supporting context:
        {context_block}

        Notes: This answer is generated without external LLM calls to keep the stack local.
        """).strip()

        return ResponseResult(answer=answer, sources=reasoning.selected_contexts)

# --------- Orchestrator ---------
class SupportCopilot:
    def __init__(self, retriever: ChromaRetriever):
        self.retriever_agent = RetrieverAgent(retriever)
        self.reasoner_agent = ReasonerAgent()
        self.responder_agent = ResponderAgent()

    def ask(self, query: str) -> ResponseResult:
        r = self.retriever_agent.run(query)
        rr = self.reasoner_agent.run(r)
        out = self.responder_agent.run(rr)
        return out
