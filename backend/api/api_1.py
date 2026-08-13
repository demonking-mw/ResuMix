# backend/api/api_1.py

"""
Hosting the API. Functionality is written elsewhere

Usage:
- Login: provided the proper info for go/up login
    - Will get a jwt token for easy reauth in the short future
-
"""

# pylint: disable=import-error
import os

from dotenv import load_dotenv
from flask import Flask, Request, request, jsonify, send_file
from flask_restful import Api
from flask_cors import CORS
from .classes.user import User
from .classes.resume import ResumeHandle
from .classes.optimize import ResumeOptimizer, ResumeOptimizerFull

import base64
from io import BytesIO

# Import your resume-related modules
from backend.src.db_helper.errors import DatabaseUnavailable
from backend.src.general_helper.json_safe import json_safe
from backend.src.general_helper.vec_rip import vec_rip
from backend.src.resume_objects.resume import Resume, ResumeGenerationError
from backend.src.resume_objects.latex_templates import LTemplate

load_dotenv()


class TolerantRequest(Request):
    """Reads query-string args even when the request has no JSON content type.

    Flask raises 415 from ``request.json`` in that case, which reqparse turns
    into a failed lookup for every argument.
    """

    def on_json_loading_failed(self, e):
        if e is None:
            return None
        return super().on_json_loading_failed(e)


app = Flask(__name__)
app.request_class = TolerantRequest


@app.before_request
def reject_non_object_json():
    """A JSON body that is not an object breaks reqparse with a TypeError."""
    if request.mimetype == "application/json" and request.content_length:
        body = request.get_json(silent=True)
        if body is not None and not isinstance(body, dict):
            return jsonify({"message": "Request body must be a JSON object"}), 400
    return None

# ---- CORS: local dev servers by default ----
# Add other origins with CORS_ORIGINS="http://host-a,http://host-b" in .env.
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
] or DEFAULT_CORS_ORIGINS

CORS(
    app,
    resources={r"/*": {"origins": CORS_ORIGINS}},
    supports_credentials=True,
)

api = Api(app)

api.add_resource(User, "/user")
api.add_resource(ResumeHandle, "/resume")
api.add_resource(ResumeOptimizer, "/resume/optimize")
api.add_resource(ResumeOptimizerFull, "/resume/optimize/full")
# api.add_resource(UserInfo, "/user/info")
# api.add_resource(Activity, "/activity")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True}), 200


@app.errorhandler(ResumeGenerationError)
def handle_generation_error(exc):
    """Turn a failed language-model or scoring step into an actionable message."""
    return jsonify({"status": False, "error_code": exc.code, "message": str(exc)}), 502


@app.errorhandler(DatabaseUnavailable)
def handle_database_error(exc):
    return (
        jsonify(
            {
                "status": False,
                "error_code": "database_unavailable",
                "message": f"The local database could not be written: {exc}",
            }
        ),
        503,
    )


@app.route("/api/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json(silent=True) or {}

    resume_dict = data.get("resume_dict")
    job_description = data.get("job_description", "")

    if not resume_dict:
        return jsonify({"error": "Missing resume_dict"}), 400

    template = LTemplate()
    my_resume = Resume(template, resume_dict)
    my_resume.make(job_description)
    my_resume.optimize()

    pdf_bytes = my_resume.build()
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume.pdf",
    )


@app.route("/api/generate-resume-full", methods=["POST"])
def generate_resume_full():
    """Return both the tailored resume dict and the PDF (base64-encoded)."""
    data = request.get_json(silent=True) or {}

    resume_dict = data.get("resume_dict")
    job_description = data.get("job_description", "")

    if not resume_dict:
        return jsonify({"error": "Missing resume_dict"}), 400

    template = LTemplate()
    my_resume = Resume(template, resume_dict)
    my_resume.make(job_description)
    my_resume.optimize()

    tailored_dict = vec_rip(json_safe(my_resume.to_tailored_dict()))
    pdf_bytes = my_resume.build()

    return jsonify({
        "resume_dict": tailored_dict,
        "resume_pdf_base64": base64.b64encode(pdf_bytes).decode("ascii"),
    })


if __name__ == "__main__":
    # Binds to loopback by default: nothing is exposed outside this machine.
    host = os.environ.get("BACKEND_HOST", "127.0.0.1")
    port = int(os.environ.get("BACKEND_PORT", os.environ.get("PORT", 5001)))
    # Opt in explicitly; the Werkzeug debugger renders tracebacks in responses.
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host=host, port=port)
