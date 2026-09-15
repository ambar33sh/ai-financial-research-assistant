import re

from app.schemas import DocumentChunk
from app.services.pdf_parser import ParsedPage


HEADING_HINTS = (
    "risk factors",
    "business",
    "financial statements",
    "management's discussion",
    "management’s discussion",
    "results of operations",
    "liquidity",
    "cash flows",
    "notes to",
    "revenue",
)


class FinancialChunker:
    """Chunk pages conservatively and retain financial-document metadata."""

    def __init__(self, target_chars: int = 1400, overlap: int = 180) -> None:
        self.target_chars = target_chars
        self.overlap = overlap

    def _section(self, text: str, current: str | None) -> str | None:
        for line in text.splitlines():
            raw = line.strip()
            normalized = re.sub(r"[^a-zA-Z'’ ]", "", raw).strip().lower()
            if not normalized:
                continue
            is_heading = normalized in HEADING_HINTS
            is_all_caps = raw == raw.upper() and any(char.isalpha() for char in raw) and len(normalized.split()) <= 7
            if is_heading or is_all_caps:
                return raw
        return current

    def chunk_pages(
        self,
        pages: list[ParsedPage],
        source_name: str,
        company: str,
        document_type: str,
        fiscal_year: int | None = None,
        document_id: str | None = None,
    ) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []
        section: str | None = None
        index = 0
        for page in pages:
            section = self._section(page.text, section)
            text = re.sub(r"\s+", " ", page.text).strip()
            start = 0
            while start < len(text):
                end = min(len(text), start + self.target_chars)
                if end < len(text):
                    boundary = max(text.rfind(". ", start, end), text.rfind("; ", start, end))
                    if boundary > start + self.target_chars // 2:
                        end = boundary + 1
                chunk_text = text[start:end].strip()
                if chunk_text:
                    chunks.append(DocumentChunk(
                        text=chunk_text,
                        page=page.page_number,
                        chunk_index=index,
                        company=company,
                        document_type=document_type,
                        fiscal_year=fiscal_year,
                        section=section,
                        source_name=source_name,
                        document_id=document_id,
                    ))
                    index += 1
                if end >= len(text):
                    break
                start = max(0, end - self.overlap)
        return chunks
