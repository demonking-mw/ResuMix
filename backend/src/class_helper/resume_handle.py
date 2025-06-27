"""
Handler for resume generate/update
Authentication only supports reauth
"""

import json
import os
import datetime
import jwt  # pylint: disable=import-error

from dotenv import load_dotenv
import psycopg  # type: ignore

from .user_auth import UserAuth
from ..db_helper import dbconn
from ..resume_objects.latex_templates import LTemplate
from ..resume_objects.resume import Resume


class ResumeHandle:
    """
    Class to deal with resume:
    Generate resume: get
    Update resume: post
    """

    def __init__(self, database: dbconn.DBConn, args: dict = None) -> None:
        """
        takes in perspective info in the form of a json with varying fields depending on actions.
        Not having a field for an action will result in failure.
        """
        self.database = database
        self.args = args

    def get_resume(self, args: dict) -> tuple[bool, bytes]:
        """
        generate resume from info stored in db
        bool is for success
        DOES NOT HANDLE SENDING FILES HERE, ONLY RETURN BYTES
        handles updating the db with cached vectors
        """
        user_auth_obj = UserAuth(self.database, args)
        user_auth_json, login_status = user_auth_obj.login_jwt()
        if (
            login_status == -1 or not user_auth_json["status"]
        ):  # Login_status SHOULD be defined if this is reached
            print("ERROR: something is cooked for login")
            return False, None
        resume_dict = user_auth_json.get("resumeinfo")
        if not resume_dict:
            print("ERROR: no resume info found for user")
            return False, None
        # Here you would generate the resume PDF from resume_dict
        templ = LTemplate()
        my_resume = Resume(templ, resume_dict)
        if not my_resume.make(args["job_description"], no_cache=args["no_cache"]):
            print("ERROR: failed to make resume")
            return False, None
        my_resume.optimize()
        resume_pdf_bytes = my_resume.build()
        new_resume_dict = my_resume.to_dict()
        if resume_dict != new_resume_dict:
            # Update the resume info in the database if there are changes
            query = f"UPDATE data SET resumeinfo = %s WHERE uid = %s"
            values = (json.dumps(new_resume_dict), user_auth_json["uid"])
            self.database.run_sql(query, values)
        return True, resume_pdf_bytes

    def set_resume_dict(self, args: dict) -> tuple[bool, str]:
        """
        Set the resume dict in the database
        bool is for success, str is for message(mainly error message)
        """
        user_auth_obj = UserAuth(self.database, args)
        user_auth_json, login_status = user_auth_obj.login_jwt()
        if (
            login_status == -1 or not user_auth_json["status"]
        ):  # Login_status SHOULD be defined if this is reached
            print("ERROR: something is cooked for login")
            return False
        new_resume_dict = args.get("resumeinfo")
        if not new_resume_dict:
            print("ERROR: no resume info provided")
            return False, "No resume info provided"
        # load it into object: if there are error, catch it here
        templ = LTemplate()
        try:
            my_resume = Resume(templ, new_resume_dict)
            if not my_resume.make(args["job_description"], no_cache=True):
                print("ERROR: failed to make resume")
                return False, "Failed to make resume"
        except Exception as e:
            print(f"ERROR: failed to load resume dict: {e}")
            return False, f"Failed to load resume dict: {str(e)}"
        processed_resume_dict = my_resume.to_dict()
        query = f"UPDATE data SET resumeinfo = %s WHERE uid = %s"
        values = (json.dumps(processed_resume_dict), user_auth_json["uid"])
        self.database.run_sql(query, values)
