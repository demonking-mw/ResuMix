"""
Database error types shared by every DBConn backend.

The application catches ``psycopg.errors.UniqueViolation`` directly, so when
psycopg is installed the local SQLite backend re-raises that exact class to stay
drop-in compatible. Without psycopg a stand-in class is used instead.
"""

try:  # pragma: no cover - depends on optional dependency
    from psycopg.errors import UniqueViolation  # type: ignore
except ImportError:  # pragma: no cover - psycopg is optional in local mode

    class UniqueViolation(Exception):
        """Raised when an insert/update violates a unique constraint."""


class DatabaseUnavailable(RuntimeError):
    """Raised when a statement could not be executed at all.

    Previously these were swallowed and reported as success, which silently
    discarded the user's edits.
    """


__all__ = ["UniqueViolation", "DatabaseUnavailable"]
