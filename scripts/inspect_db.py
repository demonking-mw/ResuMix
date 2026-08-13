"""Quick look at the local database.

Refuses to touch a remote server unless --remote is passed: DATABASE_URL in .env
may still point at a hosted database, and this should never surprise you.
"""

import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

POSTGRES_SCHEMES = ("postgres://", "postgresql://")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--remote",
        action="store_true",
        help="allow connecting to the server in DATABASE_URL",
    )
    args = parser.parse_args()

    from dotenv import load_dotenv

    load_dotenv()
    url = (os.getenv("DATABASE_URL") or "").strip()
    if url.startswith(POSTGRES_SCHEMES) and not args.remote:
        host = url.split("@")[-1].split("/")[0]
        print(
            f"DATABASE_URL points at a remote server ({host}).\n"
            "Clear it in .env to use the local file, or pass --remote to query it anyway.",
            file=sys.stderr,
        )
        return 1

    from backend.src.db_helper.dbconn import DBConn

    db = DBConn()
    try:
        rows = db.run_sql(
            "SELECT uid, user_name, email, auth_type FROM data ORDER BY uid;"
        )
        print(f"backend: {db.backend}")
        if db.backend == "sqlite":
            print(f"file:    {db.db_path}")
        print(f"users:   {len(rows)}")
        for row in rows:
            print(
                f"  {row['uid']:<20} {row['email']:<32} "
                f"{row['auth_type']:<4} {row['user_name']}"
            )
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
