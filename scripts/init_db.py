#!/usr/bin/env python3
"""
Create the local ResuMix database.

Safe to re-run: the schema is applied with CREATE TABLE IF NOT EXISTS.
Usage:
    python scripts/init_db.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from backend.src.db_helper.dbconn import DBConn  # noqa: E402


def main() -> int:
    database = DBConn()
    try:
        if database.backend != "sqlite":
            print(
                "DATABASE_URL points at a PostgreSQL server, so nothing was created "
                "locally. Apply docs/schema for hosted databases yourself, or clear "
                "DATABASE_URL in .env to use the local SQLite file."
            )
            return 0

        rows = database.run_sql("SELECT COUNT(*) AS user_count FROM data;")
        user_count = rows[0]["user_count"] if rows else 0
        print(f"Local database ready: {database.db_path}")
        print(f"Table 'data' exists with {user_count} user(s).")
        return 0
    finally:
        database.close()


if __name__ == "__main__":
    raise SystemExit(main())
