# FinSight AI Architecture

## Request flow

```text
Browser
  |
  v
Next.js frontend
  |
  v
FastAPI API
  |
  +--> PDF Parser --> Financial Chunker --> Embedding Model --> Qdrant
  |
  +--> Query Router --> Retrieval --> Reranking --> LLM --> Answer + Citations
  |
  +--> Deterministic Analytics Engine
```

## Design principles

1. Financial calculations are deterministic Python operations, not LLM-generated arithmetic.
2. Answers are grounded in retrieved document evidence.
3. Page and document metadata travel with every chunk.
4. Insufficient evidence produces an explicit limitation rather than fabricated facts.
5. The system is modular so the embedding model, reranker, vector store and LLM can be replaced independently.
