"""Shared error-to-response mapping for the REST resources.

flask-restful intercepts exceptions before Flask's ``errorhandler`` runs, so the
resources translate the known failures themselves.
"""

from backend.src.db_helper.errors import DatabaseUnavailable
from backend.src.class_helper.resume_handle import ResumeAuthenticationError
from backend.src.resume_objects.resume import ResumeGenerationError

HANDLED_ERRORS = (ResumeAuthenticationError, ResumeGenerationError, DatabaseUnavailable)


def error_response(exc) -> tuple[dict, int]:
    """Turn a known failure into a JSON body and status code."""
    if isinstance(exc, ResumeAuthenticationError):
        return {
            "status": False,
            "error_code": "reauth_required",
            "message": "ResuMix authentication expired",
        }, exc.status_code
    if isinstance(exc, ResumeGenerationError):
        return {"status": False, "error_code": exc.code, "message": str(exc)}, 400
    return {
        "status": False,
        "error_code": "database_unavailable",
        "message": f"The local database could not be written: {exc}",
    }, 503
