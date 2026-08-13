"""
Basic operations for resume
dbconn rule:
- Define it here
- Toss it around to helpers
- Helpers that takes dbconn as input has no responsibility to close it
- Usually, dbconns are closed here. MUST DOCUMENT OTHERWISE CASES.

"""

import base64
from io import BytesIO
from flask import jsonify, send_file

# pylint: disable=import-error
from flask_restful import Resource
from backend.src.db_helper.dbconn import DBConn
from backend.src.classes_req import resume_req
from backend.src.class_helper import resume_handle
from .errors import HANDLED_ERRORS, error_response


class ResumeOptimizer(Resource):
    """
    CLASS USAGE:
    update resume dict: POST
    get resume pdf: GET
    """

    def post(self) -> tuple[dict, int]:
        """
        Get the resume to download
        """
        args = resume_req.resume_get.parse_args()
        database = DBConn()
        try:
            resume_handle_obj = resume_handle.ResumeHandle(database, args)
            success, resume_pdf_bytes = resume_handle_obj.get_resume(args)
        except HANDLED_ERRORS as exc:
            return error_response(exc)
        finally:
            database.close()
        if not success:
            print("DEBUG: Failed to generate resume using resume_handle")
            return {"status": False, "message": "Failed to generate resume"}, 400
        return send_file(
            BytesIO(resume_pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="resume.pdf",
        )


class ResumeOptimizerFull(Resource):
    """Authenticated atomic structured-resume and matching-PDF endpoint."""

    def post(self):
        args = resume_req.resume_get.parse_args()
        database = DBConn()
        try:
            handler = resume_handle.ResumeHandle(database, args)
            success, result = handler.get_resume_full(args)
        except HANDLED_ERRORS as exc:
            return error_response(exc)
        finally:
            database.close()
        if not success or result is None:
            return {"status": False, "message": "Failed to generate resume"}, 400
        return jsonify({
            "status": True,
            "detail": {
                "resume_dict": result["resume_dict"],
                "resume_pdf_base64": base64.b64encode(
                    result["pdf_bytes"]
                ).decode("ascii"),
                "metadata": result["metadata"],
            },
        })
