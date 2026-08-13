from __future__ import annotations

import base64
import unittest
from unittest.mock import patch

from backend.api.api_1 import app
from backend.src.class_helper.resume_handle import (
    ResumeAuthenticationError,
    ResumeHandle,
)


class _Database:
    def __init__(self) -> None:
        self.updates = []

    def run_sql(self, query, values) -> None:
        self.updates.append((query, values))


class _Resume:
    def __init__(self, _template, resume_dict) -> None:
        self.resume_dict = resume_dict

    def make(self, _job_description, no_cache=False) -> bool:
        return True

    def optimize(self) -> None:
        return None

    def build(self) -> bytes:
        return b"%PDF-atomic-result"

    def to_tailored_dict(self) -> dict:
        return {"heading_info": {"heading_name": "Tailored"}, "sections": []}

    def to_dict(self) -> dict:
        return {"heading_info": {"heading_name": "Base"}, "sections": []}


class ResumeHandleFullTests(unittest.TestCase):
    @patch("backend.src.class_helper.resume_handle.Resume", _Resume)
    @patch("backend.src.class_helper.resume_handle.LTemplate", lambda: object())
    @patch("backend.src.class_helper.resume_handle.UserAuth")
    def test_atomic_result_contains_matching_dict_pdf_and_identity(self, auth) -> None:
        auth.return_value.login_jwt.return_value = (
            {
                "status": True,
                "uid": "user",
                "detail": {
                    "resumeinfo": {
                        "heading_info": {"heading_name": "Base"},
                        "sections": [],
                    }
                },
            },
            1,
        )
        args = {
            "uid": "user",
            "reauth_jwt": "token",
            "job_description": "Build reliable APIs",
            "no_cache": False,
        }
        handler = ResumeHandle(_Database(), args)

        success, result = handler.get_resume_full(args)
        pdf_success, pdf_bytes = handler.get_resume(args)

        self.assertTrue(success)
        self.assertEqual(result["resume_dict"]["heading_info"]["heading_name"], "Tailored")
        self.assertEqual(result["pdf_bytes"], b"%PDF-atomic-result")
        self.assertEqual(len(result["metadata"]["result_id"]), 64)
        self.assertTrue(pdf_success)
        self.assertEqual(pdf_bytes, result["pdf_bytes"])


class ResumeOptimizerFullRouteTests(unittest.TestCase):
    @patch("backend.api.classes.optimize.DBConn")
    @patch("backend.api.classes.optimize.resume_handle.ResumeHandle")
    def test_authenticated_full_route_encodes_one_handler_result(
        self, handler, database
    ) -> None:
        handler.return_value.get_resume_full.return_value = (
            True,
            {
                "resume_dict": {"sections": []},
                "pdf_bytes": b"%PDF-route",
                "metadata": {"result_id": "result-1"},
            },
        )
        response = app.test_client().post(
            "/resume/optimize/full",
            json={
                "uid": "user",
                "reauth_jwt": "token",
                "job_description": "Build reliable APIs",
                "no_cache": False,
            },
        )

        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertTrue(body["status"])
        self.assertEqual(
            base64.b64decode(body["detail"]["resume_pdf_base64"]), b"%PDF-route"
        )
        self.assertEqual(body["detail"]["metadata"]["result_id"], "result-1")
        database.return_value.close.assert_called_once()

    @patch("backend.api.classes.optimize.DBConn")
    @patch("backend.api.classes.optimize.resume_handle.ResumeHandle")
    def test_expired_auth_is_preserved_as_reauth_required(
        self, handler, database
    ) -> None:
        handler.return_value.get_resume_full.side_effect = ResumeAuthenticationError()

        response = app.test_client().post(
            "/resume/optimize/full",
            json={
                "uid": "user",
                "reauth_jwt": "expired-token",
                "job_description": "Build reliable APIs",
                "no_cache": False,
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["error_code"], "reauth_required")
        database.return_value.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()