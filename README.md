# FinSight AI

**Explainable RAG-Based Financial Research & Analysis Platform**

FinSight AI is an internship-scale financial research assistant that turns company filings and financial reports into searchable, evidence-grounded answers and deterministic financial analysis.

## Core capabilities

- Upload PDF financial reports
- Extract and structure document text with page metadata
- Structure-aware chunking with section detection
- Semantic vector retrieval with Qdrant
- Hybrid retrieval using vector similarity + candidate-set BM25
- Cross-encoder reranking
- RAG answers with page-level citations
- Lightweight query-intent routing for research, analytics, and hybrid queries
- Deterministic financial ratio and growth calculations
- Deterministic company comparison endpoint
- Explainable financial red-flag detection
- Persistent document metadata registry
- Evaluation scaffolding and automated tests

> **Routing note:** Query routing currently classifies intent and is exposed in the API response. It does not yet automatically extract financial values from natural-language questions and execute a calculation. Structured calculations are available through the deterministic analytics endpoints.

## Architecture

```text
PDF -> Parser -> Chunker -> Embeddings -> Qdrant
                         |                    |
                         +-> Document Registry |
                                              |
Question -> Intent Router -> Hybrid Retriever -> Cross-Encoder
                                      |                 |
                                      +-------------> Grounded LLM
                                                        |
                                              Citations / Evidence

Structured financial inputs -> Deterministic Analytics -> Metrics / Risks / Comparison
```

## Tech stack

- Backend: Python, FastAPI, Pydantic
- Retrieval: Qdrant, Sentence Transformers, BM25, cross-encoder reranking
- LLM: OpenAI-compatible API
- Frontend: Next.js, TypeScript
- Tests: pytest
- Local infrastructure: Docker Compose
- Metadata persistence: SQLite registry

## Quick start

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
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

## API highlights

- `GET /api/v1/health` — health check
- `POST /api/v1/documents` — ingest and index a PDF
- `GET /api/v1/documents` — list registered documents
- `GET /api/v1/documents/{document_id}` — retrieve document metadata
- `POST /api/v1/search` — hybrid document retrieval
- `POST /api/v1/ask` — grounded research answer with citations
- `POST /api/v1/analytics/metrics` — deterministic financial metrics
- `POST /api/v1/analytics/risks` — deterministic financial risk flags
- `POST /api/v1/analytics/compare` — deterministic company comparison

## Environment variables

See `backend/.env.example`. Never commit real API keys.

## Current scope

The first implementation is deliberately focused on a small set of financial documents. Add annual/quarterly reports for Apple, Microsoft and NVIDIA through the upload interface. Do not commit copyrighted reports to the repository unless redistribution rights permit it.

## Disclaimer

FinSight AI is an educational/research prototype, not investment advice. Financial figures should be verified against the cited source documents.
