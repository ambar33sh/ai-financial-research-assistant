# Methodology

## 1. Document ingestion

Users upload PDF financial reports. The API validates file type and size, stores the document outside version control, extracts page-level text and rejects PDFs with no readable text.

## 2. Structure-aware chunking

Text is normalized and divided into bounded chunks while retaining page number, source name, company, reporting year, document type and a section hint.

## 3. Retrieval

Each chunk is embedded into a vector representation and stored in Qdrant. The architecture is designed for hybrid retrieval: semantic search can be combined with lexical matching and a reranker as the retrieval layer matures.

## 4. Grounded generation

The question router identifies research, analytics or hybrid intent. Research questions retrieve evidence and pass it to the LLM with a strict grounding instruction. Citations are generated from retrieved metadata, not invented by the model.

## 5. Financial analytics

Core financial metrics use explicit formulas in Python. This keeps arithmetic reproducible and makes calculation behavior unit-testable.

## 6. Risk intelligence

Risk detection will combine deterministic financial signals with evidence extracted from management discussion and risk sections. Any displayed risk should retain a source reference.
