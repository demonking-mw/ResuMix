"""
DBConn is the single database entry point used by the whole application.

Local-first default: with no configuration at all, ResuMix stores everything in
a SQLite file under ``data/resumix.db``. Nothing needs to be provisioned and no
network access is required.

Selecting a backend (via DATABASE_URL, usually in .env):
    unset / empty          -> SQLite at RESUMIX_DB_PATH or <repo>/data/resumix.db
    sqlite:///./data/x.db  -> SQLite at that path
    postgresql://user@host -> PostgreSQL (hosted deployments only)

Sample usage:
database = dbconn.DBConn()
table_1 = database.run_sql('SELECT * FROM data;')
database.close()

Note: can swap the exact code out for different database or for prod.
Functions must remain the same
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from .sqlite_conn import SQLiteConn

# backend/src/db_helper/dbconn.py -> repository root
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = REPO_ROOT / "data" / "resumix.db"

POSTGRES_SCHEMES = ("postgres://", "postgresql://")
SQLITE_SCHEMES = ("sqlite://", "sqlite3://")


def resolve_sqlite_path(database_url: str = "") -> Path:
    """
    Work out which SQLite file to use, in precedence order:
    DATABASE_URL (sqlite scheme) > RESUMIX_DB_PATH > <repo>/data/resumix.db
    """
    lowered = database_url.lower()
    for scheme in SQLITE_SCHEMES:
        if lowered.startswith(scheme):
            raw_path = database_url[len(scheme) :]
            # sqlite:///relative/path and sqlite:////absolute/path
            if raw_path.startswith("/"):
                raw_path = raw_path[1:]
            if raw_path:
                path = Path(raw_path).expanduser()
                return path if path.is_absolute() else (REPO_ROOT / path).resolve()

    override = os.getenv("RESUMIX_DB_PATH", "").strip()
    if override:
        path = Path(override).expanduser()
        return path if path.is_absolute() else (REPO_ROOT / path).resolve()

    return DEFAULT_DB_PATH


class DBConn:
    """
    DBConn class to open a database connection and run SQL queries.
    Call close() when finished.
    """

    def __init__(self) -> None:
        """
        Pick the backend from the environment and connect to it
        """
        load_dotenv()
        self.connection_string = (os.getenv("DATABASE_URL") or "").strip()

        if self.connection_string.lower().startswith(POSTGRES_SCHEMES):
            # Imported here so local installs never need psycopg at runtime.
            from .postgres_conn import PostgresConn

            sslmode = os.getenv("DATABASE_SSLMODE", "require").strip() or "require"
            self.backend = "postgres"
            self.db_path = None
            self._impl = PostgresConn(self.connection_string, sslmode=sslmode)
        else:
            self.backend = "sqlite"
            self.db_path = resolve_sqlite_path(self.connection_string)
            self._impl = SQLiteConn(self.db_path)

    def run_sql(self, sql_query: str, params=None) -> list:
        """
        Run SQL query and return the resulting rows as a list of dicts
        return empty list if no result or status is false
        """
        return self._impl.run_sql(sql_query, params)

    def close(self) -> None:
        """
        Release the underlying connection(s)
        """
        self._impl.close()
