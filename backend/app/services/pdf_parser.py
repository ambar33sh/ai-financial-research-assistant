from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass
class ParsedPage:
    page_number: int
    text: str


class PDFParser:
    """Extract readable page-level text while retaining source page numbers."""

    def parse(self, path: Path) -> list[ParsedPage]:
        pages: list[ParsedPage] = []
        with fitz.open(path) as document:
            for index, page in enumerate(document):
                text = page.get_text("text").strip()
                if text:
                    pages.append(ParsedPage(page_number=index + 1, text=text))
        return pages
