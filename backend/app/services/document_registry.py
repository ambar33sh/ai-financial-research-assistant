import sqlite3
from pathlib import Path
from threading import Lock

from app.config import get_settings
from app.schemas import DocumentInfo


class DocumentRegistry:
    """Small local registry for document lifecycle metadata.

    SQLite keeps the internship project self-contained. The repository can later be
    swapped for PostgreSQL without changing the API contract.
    """

    def __init__(self) -> None:
        db_path = Path(get_settings().upload_dir).parent / "finsight.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._lock = Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    source_name TEXT NOT NULL,
                    company TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    fiscal_year INTEGER,
                    pages INTEGER NOT NULL,
                    chunks INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add(self, document: DocumentInfo) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """INSERT INTO documents
                (document_id, source_name, company, document_type, fiscal_year, pages, chunks)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (document.document_id, document.source_name, document.company, document.document_type,
                 document.fiscal_year, document.pages, document.chunks),
            )

    def get(self, document_id: str) -> DocumentInfo | None:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM documents WHERE document_id = ?", (document_id,)).fetchone()
        return DocumentInfo(**dict(row)) if row else None

    def list(self) -> list[DocumentInfo]:
        with self._lock, self._connect() as conn:
            rows = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
        return [DocumentInfo(**dict(row)) for row in rows]

    def delete(self, document_id: str) -> bool:
        with self._lock, self._connect() as conn:
            cursor = conn.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
        return cursor.rowcount > 0
