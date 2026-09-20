import sqlite3
from datetime import UTC, datetime

from pydantic import BaseModel

from app.tools import PermissionLevel


class WorkItem(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str


class WorkItemStore:
    PERMISSIONS: dict[str, PermissionLevel] = {
        "create": PermissionLevel.WRITE,
        "get": PermissionLevel.READ,
        "list": PermissionLevel.READ,
        "update": PermissionLevel.WRITE,
        "delete": PermissionLevel.DESTRUCTIVE,
    }

    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS work_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def _row_to_item(self, row: sqlite3.Row) -> WorkItem:
        return WorkItem(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def create(self, title: str, description: str = "") -> WorkItem:
        now = datetime.now(UTC).isoformat()
        cursor = self._conn.execute(
            "INSERT INTO work_items (title, description, status, created_at, updated_at) "
            "VALUES (?, ?, 'open', ?, ?)",
            (title, description, now, now),
        )
        self._conn.commit()
        assert cursor.lastrowid is not None
        item = self.get(cursor.lastrowid)
        assert item is not None
        return item

    def get(self, item_id: int) -> WorkItem | None:
        row = self._conn.execute(
            "SELECT * FROM work_items WHERE id = ?", (item_id,)
        ).fetchone()
        return self._row_to_item(row) if row else None

    def list(self, status: str | None = None) -> list[WorkItem]:
        if status is None:
            rows = self._conn.execute("SELECT * FROM work_items ORDER BY id").fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM work_items WHERE status = ? ORDER BY id", (status,)
            ).fetchall()
        return [self._row_to_item(row) for row in rows]

    def update(self, item_id: int, **fields: str) -> WorkItem | None:
        if self.get(item_id) is None:
            return None
        allowed = {"title", "description", "status"}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if updates:
            set_clause = ", ".join(f"{k} = ?" for k in updates)
            values = [*updates.values(), datetime.now(UTC).isoformat(), item_id]
            self._conn.execute(
                f"UPDATE work_items SET {set_clause}, updated_at = ? WHERE id = ?", values
            )
            self._conn.commit()
        return self.get(item_id)

    def delete(self, item_id: int) -> bool:
        if self.get(item_id) is None:
            return False
        self._conn.execute("DELETE FROM work_items WHERE id = ?", (item_id,))
        self._conn.commit()
        return True
