"""
SQLite backend for DBConn: the default store when ResuMix runs locally.

No server, no credentials, no network. The database is a single file that is
created (with its schema) the first time it is opened.

Compatibility notes with the PostgreSQL backend:
  - ``%s`` placeholders are rewritten to SQLite's ``?``.
  - dict/list parameters are JSON-encoded on write.
  - ``userinfo`` / ``resumeinfo`` are JSON-decoded on read, so callers keep
    receiving dicts exactly as psycopg returns for JSONB columns.
  - unique-constraint failures raise the same UniqueViolation the API catches.
"""

import json
import sqlite3
import threading
from pathlib import Path

from .errors import DatabaseUnavailable, UniqueViolation

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

# Columns held as JSONB in PostgreSQL and as TEXT in SQLite.
JSON_COLUMNS = ("userinfo", "resumeinfo")


def _encode_params(params) -> tuple:
    """JSON-encode dict/list values so they can be bound as TEXT."""
    if params is None:
        return ()
    if isinstance(params, (str, bytes)):
        return (params,)
    return tuple(
        json.dumps(value) if isinstance(value, (dict, list)) else value
        for value in params
    )


def _decode_row(row: sqlite3.Row) -> dict:
    """Turn a row into a dict, restoring JSON columns to Python objects."""
    record = dict(row)
    for column in JSON_COLUMNS:
        value = record.get(column)
        if isinstance(value, (str, bytes)):
            try:
                record[column] = json.loads(value)
            except (TypeError, ValueError):
                pass
    return record


def translate_placeholders(sql_query: str, has_params: bool) -> str:
    """Rewrite psycopg's ``%s`` placeholders as SQLite's ``?``.

    Only outside string literals: a plain replace turns ``LIKE '%stuff%'`` into
    ``LIKE '?tuff%'``, which silently matches nothing. Like psycopg, ``%`` is
    only special when parameters are supplied, and ``%%`` means a literal ``%``.
    """
    if not has_params:
        return sql_query

    out = []
    quote = None
    index = 0
    while index < len(sql_query):
        char = sql_query[index]
        if quote:
            out.append(char)
            if char == quote:
                if index + 1 < len(sql_query) and sql_query[index + 1] == quote:
                    out.append(quote)  # doubled quote escapes itself
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char in ("'", '"'):
            quote = char
            out.append(char)
            index += 1
            continue
        if char == "%" and index + 1 < len(sql_query):
            following = sql_query[index + 1]
            if following == "s":
                out.append("?")
                index += 2
                continue
            if following == "%":
                out.append("%")
                index += 2
                continue
        out.append(char)
        index += 1
    return "".join(out)


class SQLiteConn:
    """
    Local file-backed implementation of the DBConn interface.
    Exposes the same run_sql/close surface as the PostgreSQL backend.
    """

    def __init__(self, db_path) -> None:
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        # A single connection is shared by the Flask threads that use this object.
        self._lock = threading.Lock()
        self.connection.execute("PRAGMA journal_mode=WAL;")
        self.connection.execute("PRAGMA foreign_keys=ON;")
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create the tables on first use so a fresh clone just works."""
        try:
            with self._lock:
                self.connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
                self.connection.commit()
        except sqlite3.Error as exc:
            raise DatabaseUnavailable(
                f"Could not open {self.db_path} for writing: {exc}"
            ) from exc

    def run_sql(self, sql_query: str, params=None) -> list:
        """
        Run one SQL statement and return the result rows as dicts.
        Returns an empty list for statements that produce no rows.
        Raises DatabaseUnavailable if the statement could not be executed.
        """
        statement = translate_placeholders(sql_query, params is not None)
        bound = _encode_params(params)
        try:
            with self._lock:
                cursor = self.connection.execute(statement, bound)
                results = (
                    [_decode_row(row) for row in cursor.fetchall()]
                    if cursor.description is not None
                    else []
                )
                self.connection.commit()
                cursor.close()
        except sqlite3.IntegrityError as exc:
            self.connection.rollback()
            if "UNIQUE constraint failed" in str(exc):
                raise UniqueViolation(str(exc)) from exc
            raise
        except sqlite3.Error as exc:
            try:
                self.connection.rollback()
            except sqlite3.Error:
                pass
            print(f"Database error: {exc}")
            raise DatabaseUnavailable(str(exc)) from exc
        return results

    def close(self) -> None:
        """Close the underlying connection."""
        self.connection.close()
