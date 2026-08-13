"""
Handler for resume generate/update
Authentication only supports reauth
"""

import json
import os
import datetime
import hashlib
import jwt  # pylint: disable=import-error

from dotenv import load_dotenv

from .user_auth import UserAuth
from ..db_helper import dbconn
from ..general_helper.json_safe import json_safe
from ..general_helper.vec_rip import vec_rip
from ..resume_objects.latex_templates import LTemplate
from ..resume_objects.resume import Resume


class ResumeAuthenticationError(RuntimeError):
    """Raised when a resume request needs a fresh reauthentication token."""

    def __init__(self, status_code: int = 401) -> None:
        super().__init__("ResuMix reauthentication required")
        self.status_code = status_code


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
        return json_safe(obj)

    def __carry_over_vectors(self, uid: str, incoming: dict) -> None:
        """Re-attach cached embeddings to lines whose text did not change.

        The editor never sees the vectors (vec_rip strips them), so a plain save
        would throw the whole cache away and make the next generation re-embed
        every line.
        """
        rows = self.database.run_sql(
            "SELECT resumeinfo FROM data WHERE uid = %s;", (uid,)
        )
        if not rows:
            return
        stored = rows[0]["resumeinfo"]
        if isinstance(stored, str):
            try:
                stored = json.loads(stored)
            except (TypeError, ValueError):
                return
        if not isinstance(stored, dict):
            return

        cached = {}
        for line in _iter_lines(stored):
            vector = line.get("aux_info", {}).get("vec")
            if vector is not None:
                cached[line.get("content_str", "")] = vector
        if not cached:
            return

        for line in _iter_lines(incoming):
            vector = cached.get(line.get("content_str", ""))
            if vector is not None and "vec" not in line.setdefault("aux_info", {}):
                line["aux_info"]["vec"] = vector

    def __save_cached_vectors(self, uid: str, loaded: dict, scored: dict) -> None:
        """Persist the embeddings and scores computed during generation.

        Generation takes seconds, and the only thing being written back is a
        cache. If the user saved an edit while it ran, that edit is newer than
        what we are holding, so the write is skipped rather than clobbering it.
        """
        try:
            if json.dumps(loaded, sort_keys=True) == json.dumps(scored, sort_keys=True):
                return
        except (TypeError, ValueError) as exc:
            print(f"WARNING: could not compare resume dictionaries: {exc}")

        current = self.database.run_sql(
            "SELECT resumeinfo FROM data WHERE uid = %s;", (uid,)
        )
        if not current:
            return
        stored = current[0]["resumeinfo"]
        if isinstance(stored, str):
            try:
                stored = json.loads(stored)
            except (TypeError, ValueError):
                stored = None
        try:
            unchanged = json.dumps(json_safe(stored), sort_keys=True) == json.dumps(
                loaded, sort_keys=True
            )
        except (TypeError, ValueError):
            unchanged = False
        if not unchanged:
            print("INFO: resume changed during generation; skipping the vector cache write")
            return

        self.database.run_sql(
            "UPDATE data SET resumeinfo = %s WHERE uid = %s",
            (json.dumps(scored), uid),
        )

    def get_resume(self, args: dict) -> tuple[bool, bytes]:
        """
        generate resume from info stored in db
        bool is for success
        DOES NOT HANDLE SENDING FILES HERE, ONLY RETURN BYTES
        handles updating the db with cached vectors
        """
        success, result = self.get_resume_full(args)
        return success, result["pdf_bytes"] if success else None

    def get_resume_full(self, args: dict) -> tuple[bool, dict | None]:
        """Return one authenticated tailored-dict/PDF result from one Resume.

        The existing :meth:`get_resume` API delegates here and keeps returning
        PDF bytes for compatibility. Identity hashes let clients prove the
        structured projection and PDF came from this same optimization call.
        """
        user_auth_obj = UserAuth(self.database, args)
        user_auth_json, login_status = user_auth_obj.login_jwt()
        if login_status in (401, 403):
            raise ResumeAuthenticationError(login_status)
        if (
            login_status == -1 or not user_auth_json["status"]
        ):  # Login_status SHOULD be defined if this is reached
            print("ERROR: something is cooked for login")
            return False, None
        # Prefer the stored row: the auth payload has been through vec_rip, so
        # it carries no cached embeddings to reuse.
        resumeinfo_raw = None
        try:
            stored_rows = self.database.run_sql(
                "SELECT resumeinfo FROM data WHERE uid = %s;", (args["uid"],)
            )
        except Exception:  # noqa: BLE001 - fall back to what auth already gave us
            stored_rows = None
        if stored_rows:
            resumeinfo_raw = stored_rows[0].get("resumeinfo")
        if not resumeinfo_raw:
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
        # Convert the original resume_dict for proper comparison
        converted_resume_dict = self.__convert_ndarray(resume_dict)
        # Here you would generate the resume PDF from resume_dict
        templ = LTemplate()
        my_resume = Resume(templ, resume_dict)
        if not my_resume.make(args["job_description"], no_cache=args["no_cache"]):
            print("ERROR: failed to make resume")
            return False, None
        my_resume.optimize()
        resume_pdf_bytes = my_resume.build()
        # Cached embeddings are several hundred KB and of no use to a client.
        tailored_resume_dict = vec_rip(
            self.__convert_ndarray(my_resume.to_tailored_dict())
        )
        new_resume_dict = my_resume.to_dict()
        new_resume_dict = self.__convert_ndarray(new_resume_dict)

        self.__save_cached_vectors(args["uid"], converted_resume_dict, new_resume_dict)

        base_resume_hash = _json_hash(converted_resume_dict)
        job_description_hash = hashlib.sha256(
            args["job_description"].strip().encode("utf-8")
        ).hexdigest()
        tailored_resume_hash = _json_hash(tailored_resume_dict)
        pdf_hash = hashlib.sha256(resume_pdf_bytes).hexdigest()
        result_id = hashlib.sha256(
            "|".join(
                (
                    base_resume_hash,
                    job_description_hash,
                    tailored_resume_hash,
                    pdf_hash,
                )
            ).encode("ascii")
        ).hexdigest()
        return True, {
            "resume_dict": tailored_resume_dict,
            "pdf_bytes": resume_pdf_bytes,
            "metadata": {
                "result_id": result_id,
                "base_resume_hash": base_resume_hash,
                "job_description_hash": job_description_hash,
                "tailored_resume_hash": tailored_resume_hash,
                "pdf_hash": pdf_hash,
            },
        }

    def set_resume_dict(self, args: dict) -> tuple[bool, str]:
        """
        Set the resume dict in the database
        bool is for success, str is for message(mainly error message)
        """
        user_auth_obj = UserAuth(self.database, args)
        user_auth_json, login_status = user_auth_obj.login_jwt()
        if login_status in (401, 403):
            raise ResumeAuthenticationError(login_status)
        if (
            login_status == -1 or not user_auth_json["status"]
        ):  # Login_status SHOULD be defined if this is reached
            print("ERROR: something is cooked for login")
            return False, "Not authenticated"
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

        # # load it into object: if there are error, catch it here
        # templ = LTemplate()
        # try:
        #     my_resume = Resume(templ, new_resume_dict)
        #     if not my_resume.make(
        #         "This is a backend software engineer role, where the candidate will be instrumental in developing, hosting, and maintaining the robust server-side infrastructure and APIs on the cloud (AWS) that power our diverse applications. The candidate should have strong experience in backend development, especially with languages like Python (e.g., Django, Flask), Java (e.g., Spring Boot), or Node.js (e.g., Express). They should also be deeply familiar with designing and managing various databases (both relational like PostgreSQL or MySQL, and NoSQL like MongoDB or Redis) and possess a solid understanding of scalable architecture, API security, and distributed systems.",
        #         no_cache=True,
        #     ):
        #         print("ERROR: failed to make resume")
        #         return False, "Failed to make resume"
        # except (TypeError, ValueError) as e:
        #     print(f"ERROR: failed to load resume dict: {e}")
        #     return False, f"Failed to load resume dict: {str(e)}"
        processed_resume_dict = self.__convert_ndarray(new_resume_dict)
        self.__carry_over_vectors(args["uid"], processed_resume_dict)
        query = "UPDATE data SET resumeinfo = %s WHERE uid = %s"
        values = (json.dumps(processed_resume_dict), args["uid"])
        self.database.run_sql(query, values)
        return True, "Resume updated successfully"


def _json_hash(value: dict) -> str:
    payload = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _iter_lines(resume: dict):
    """Yield every line dict in a resume, tolerating a partial structure."""
    for section in resume.get("sections", []) or []:
        for item in section.get("items", []) or []:
            for line in item.get("lines", []) or []:
                if isinstance(line, dict):
                    yield line
