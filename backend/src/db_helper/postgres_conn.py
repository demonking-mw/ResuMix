"""
PostgreSQL backend for DBConn: used only when DATABASE_URL points at a server.

This is the original hosted-deployment code path. Local runs never import
psycopg because this module is imported lazily by dbconn.py.
"""

import psycopg
from psycopg_pool import ConnectionPool
from psycopg.errors import QueryCanceled, OperationalError

from .errors import DatabaseUnavailable


class PostgresConn:
    """
    Connection-pool implementation of the DBConn interface.
    """

    def __init__(self, connection_string: str, sslmode: str = "require") -> None:
        self.connection_string = connection_string
        self.conn_pool = ConnectionPool(
            self.connection_string, kwargs={"sslmode": sslmode}
        )

    def run_sql(self, sql_query: str, params=None) -> list:
        """
        Run SQL query on existing connection pool
        return empty list if the statement produced no rows
        Raises DatabaseUnavailable if the statement could not be executed.
        """
        try:
            with self.conn_pool.connection() as conn:
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                    cur.execute(sql_query, params)
                    results = []
                    if cur.description is not None:
                        results = cur.fetchall()
                    else:
                        conn.commit()
        except (QueryCanceled, OperationalError) as e:
            print(f"Database error: {e}")
            raise DatabaseUnavailable(str(e)) from e
        return results

    def close(self) -> None:
        """
        Close all connections in the pool
        """
        self.conn_pool.close()
