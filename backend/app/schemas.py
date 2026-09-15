from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    text: str
    page: int = Field(ge=1)
    chunk_index: int = Field(ge=0)
    company: str
    document_type: str
    fiscal_year: int | None = None
    section: str | None = None
    source_name: str


class IngestResponse(BaseModel):
    document_id: str
    source_name: str
    pages: int
    chunks: int
    indexed: bool


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    company: str | None = None
    fiscal_year: int | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    text: str
    score: float
    page: int
    source_name: str
    company: str
    fiscal_year: int | None = None
    section: str | None = None


class AskRequest(SearchRequest):
    conversation_id: str | None = None


class Citation(BaseModel):
    source_name: str
    page: int
    section: str | None = None
    evidence: str


class AskResponse(BaseModel):
    answer: str
    route: str
    citations: list[Citation]
    evidence_strength: str
    calculation: dict | None = None


class MetricsRequest(BaseModel):
    revenue: float | None = None
    previous_revenue: float | None = None
    beginning_revenue: float | None = None
    years: float | None = Field(default=None, gt=0)
    gross_profit: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    free_cash_flow: float | None = None
    debt: float | None = None
    equity: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    quick_assets: float | None = None
    average_equity: float | None = None
    average_assets: float | None = None
    invested_capital: float | None = None
