"""
Basic operations for resume
dbconn rule:
- Define it here
- Toss it around to helpers
- Helpers that takes dbconn as input has no responsibility to close it
- Usually, dbconns are closed here. MUST DOCUMENT OTHERWISE CASES.

"""

from io import BytesIO
from flask import send_file

# pylint: disable=import-error
from flask_restful import Resource
from backend.src.db_helper.dbconn import DBConn
from backend.src.classes_req import resume_req
from backend.src.class_helper import resume_handle
from backend.src.general_helper.google_auth_extract import GoogleAuthExtract as gae


class ResumeHandle(Resource):
    """
    CLASS USAGE:
    update resume dict: POST
    get resume pdf: GET
    """

    def get(self) -> tuple[dict, int]:
        """
        Get the resume to download
        """
        args = resume_req.resume_get.parse_args()
        database = DBConn()
        resume_handle_obj = resume_handle.ResumeHandle(database, args)
        success, resume_pdf_bytes = resume_handle_obj.get_resume(args)
        database.close()
        if not success:
            return {"status": False, "message": "Failed to generate resume"}, 400
        return send_file(
            BytesIO(resume_pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="resume.pdf",
        )

    def post(self) -> tuple[dict, int]:
        """
        Set resume dict
        Process the input, set cache vectors
        Return status only
        """
        args = resume_req.resume_post.parse_args()
        database = DBConn()
        resume_handle_obj = resume_handle.ResumeHandle(database, args)
        success, message = resume_handle_obj.set_resume_dict(args)
        database.close()
        if not success:
            return {"status": False, "message": message}, 400
        {"status": True, "message": f"Resume updated successfully: {message}"}, 200
