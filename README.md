# FinSight AI

**Explainable RAG-Based Financial Research & Analysis Platform**

FinSight AI is an internship-scale financial research assistant that turns company filings and financial reports into searchable, evidence-grounded answers and deterministic financial analysis.

## Core capabilities

- Upload PDF financial reports
- Extract and structure document text with page metadata
- Structure-aware chunking
- Semantic vector retrieval with Qdrant
- Hybrid retrieval with keyword scoring
- Cross-encoder reranking
- RAG answers with page-level citations
- Query routing between research, analytics, and hybrid workflows
- Deterministic financial ratio and growth calculations
- Company comparison
- Explainable red-flag detection
- Evaluation and automated tests

## Architecture

```text
PDF -> Parser -> Chunker -> Embeddings -> Qdrant
                                         |
Question -> Router -> Retriever -> Reranker
                       |                 |
                       +--> Analytics ---+
                              |
                           LLM Answer
                              |
                         Citations/Evidence
```

## Tech stack

- Backend: Python, FastAPI, Pydantic
- Retrieval: Qdrant, Sentence Transformers
- LLM: OpenAI-compatible API
- Frontend: Next.js, TypeScript, Tailwind CSS
- Tests: pytest
- Local infrastructure: Docker Compose

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
uvicorn app.main:app --reload
```

### Infrastructure

```bash
docker compose up -d qdrant
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Environment variables

See `backend/.env.example`. Never commit real API keys.

## Current scope

The first implementation is deliberately focused on a small set of financial documents. Add annual/quarterly reports for Apple, Microsoft and NVIDIA through the upload interface. Do not commit copyrighted reports to the repository unless redistribution rights permit it.

## Disclaimer

FinSight AI is an educational/research prototype, not investment advice. Financial figures should be verified against the cited source documents.
