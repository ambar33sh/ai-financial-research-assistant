from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.schemas import AskRequest, AskResponse, DocumentInfo, IngestResponse, SearchRequest, SearchResult
from app.services.chunker import FinancialChunker
from app.services.document_registry import DocumentRegistry
from app.services.hybrid_retriever import HybridRetriever
from app.services.llm import LLMService
from app.services.pdf_parser import PDFParser
from app.services.query_router import QueryRouter
from app.services.vector_store import VectorStore

router = APIRouter()
parser = PDFParser()
chunker = FinancialChunker()
store = VectorStore()
hybrid_retriever = HybridRetriever()
llm = LLMService()
router_service = QueryRouter()
registry = DocumentRegistry()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "finsight-backend"}


@router.get("/documents", response_model=list[DocumentInfo])
def list_documents() -> list[DocumentInfo]:
    return registry.list()


@router.get("/documents/{document_id}", response_model=DocumentInfo)
def get_document(document_id: str) -> DocumentInfo:
    document = registry.get(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.post("/documents", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    company: str = Form(...),
    document_type: str = Form("financial_report"),
    fiscal_year: int | None = Form(None),
) -> IngestResponse:
    settings = get_settings()
    company = company.strip()
    document_type = document_type.strip()
    if not company:
        raise HTTPException(status_code=422, detail="Company is required")
    if not document_type:
        raise HTTPException(status_code=422, detail="Document type is required")
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF documents are supported")

    contents = await file.read()
    if len(contents) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.max_upload_mb} MB limit")

    document_id = str(uuid4())
    safe_name = Path(file.filename or "document.pdf").name
    path = settings.upload_path / f"{document_id}_{safe_name}"
    path.write_bytes(contents)
    try:
        pages = parser.parse(path)
        if not pages:
            raise HTTPException(status_code=422, detail="No readable text was found in the PDF")
        chunks = chunker.chunk_pages(
            pages, safe_name, company, document_type, fiscal_year, document_id=document_id
        )
        indexed = store.upsert(chunks) == len(chunks)
        if not indexed:
            raise HTTPException(status_code=503, detail="Document indexing was incomplete")
        registry.add(DocumentInfo(
            document_id=document_id,
            source_name=safe_name,
            company=company,
            document_type=document_type,
            fiscal_year=fiscal_year,
            pages=len(pages),
            chunks=len(chunks),
        ))
        return IngestResponse(
            document_id=document_id,
            source_name=safe_name,
            pages=len(pages),
            chunks=len(chunks),
            indexed=True,
        )
    except HTTPException:
        path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Document ingestion failed: {exc}") from exc


@router.post("/search", response_model=list[SearchResult])
def search(request: SearchRequest) -> list[SearchResult]:
    return hybrid_retriever.retrieve(request.query, request.top_k, request.company, request.fiscal_year)


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    route = router_service.route(request.query)
    results = hybrid_retriever.retrieve(request.query, request.top_k, request.company, request.fiscal_year)
    answer, citations, strength = llm.answer(request.query, results)
    return AskResponse(answer=answer, route=route, citations=citations, evidence_strength=strength)
