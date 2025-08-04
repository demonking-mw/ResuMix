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

    def __convert_ndarray(self, obj):
        """
        get the resume info object ready for json serialization
        """
        try:
            import numpy as np
        except ImportError:
            np = None
        if np and isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: self.__convert_ndarray(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.__convert_ndarray(v) for v in obj]
        else:
            return obj

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
        resumeinfo_raw = user_auth_json["detail"].get("resumeinfo")
        if isinstance(resumeinfo_raw, str):
            try:
                resume_dict = json.loads(resumeinfo_raw)
            except Exception:
                print("ERROR: resumeinfo could not be decoded from JSON string")
                resume_dict = None
        else:
            resume_dict = resumeinfo_raw
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
        new_resume_dict = self.__convert_ndarray(new_resume_dict)

        # Convert the original resume_dict for proper comparison
        converted_resume_dict = self.__convert_ndarray(resume_dict)

        # Use JSON serialization for safe comparison of complex dictionaries
        try:
            if json.dumps(converted_resume_dict, sort_keys=True) != json.dumps(
                new_resume_dict, sort_keys=True
            ):
                # Update the resume info in the database if there are changes
                print("DEBUG: hashing resume info to db")
                query = "UPDATE data SET resumeinfo = %s WHERE uid = %s"
                values = (json.dumps(new_resume_dict), user_auth_json["uid"])
                self.database.run_sql(query, values)
        except (TypeError, ValueError) as e:
            # If JSON serialization fails, fall back to assuming they're different
            print(
                f"WARNING: Could not compare resume dictionaries, updating anyway: {e}"
            )
            query = "UPDATE data SET resumeinfo = %s WHERE uid = %s"
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

        # Check if resume has any items
        has_items = False
        sections = new_resume_dict.get("sections", [])
        for section in sections:
            items = section.get("items", [])
            for item in items:
                aux_info = item.get("aux_info", {})
                if aux_info.get("type") == "items":
                    has_items = True
                    break
            if has_items:
                break

        if not has_items:
            print("ERROR: resume has no items")
            return False, "Empty resume - no items found"

        # load it into object: if there are error, catch it here
        templ = LTemplate()
        try:
            my_resume = Resume(templ, new_resume_dict)
            if not my_resume.make(
                "This is a backend software engineer role, where the candidate will be instrumental in developing, hosting, and maintaining the robust server-side infrastructure and APIs on the cloud (AWS) that power our diverse applications. The candidate should have strong experience in backend development, especially with languages like Python (e.g., Django, Flask), Java (e.g., Spring Boot), or Node.js (e.g., Express). They should also be deeply familiar with designing and managing various databases (both relational like PostgreSQL or MySQL, and NoSQL like MongoDB or Redis) and possess a solid understanding of scalable architecture, API security, and distributed systems.",
                no_cache=True,
            ):
                print("ERROR: failed to make resume")
                return False, "Failed to make resume"
        except (TypeError, ValueError) as e:
            print(f"ERROR: failed to load resume dict: {e}")
            return False, f"Failed to load resume dict: {str(e)}"
        processed_resume_dict = my_resume.to_dict()
        query = "UPDATE data SET resumeinfo = %s WHERE uid = %s"
        print("DEBUG: resume to_dict: type of " + str(type(processed_resume_dict)))
        processed_resume_dict = self.__convert_ndarray(processed_resume_dict)
        values = (json.dumps(processed_resume_dict), args["uid"])
        self.database.run_sql(query, values)
        return True, "Resume updated successfully"
