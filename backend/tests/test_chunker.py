from app.services.chunker import FinancialChunker
from app.services.pdf_parser import ParsedPage


def test_chunker_preserves_page_and_source_metadata():
    pages = [ParsedPage(page_number=3, text="Risk Factors\n" + "Revenue concentration may affect results. " * 20)]
    chunks = FinancialChunker(target_chars=200, overlap=20).chunk_pages(
        pages, "apple-2025.pdf", "Apple", "10-K", 2025
    )
    assert chunks
    assert all(chunk.page == 3 for chunk in chunks)
    assert all(chunk.source_name == "apple-2025.pdf" for chunk in chunks)
    assert all(chunk.company == "Apple" for chunk in chunks)
