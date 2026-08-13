"""
Handler for user authentication situations with every login process
Login options: uid/password (up), email/password (ep), google oauth (go)
Signup options: username/password/email (upe), email/password (ep), google oauth (go)
Note: email smtp not supported, yet

On database: eup for email/username/password, go for google oauth
DATABASE: USE PROVIDED, DO NOT CLOSE

Note: for each method, doccumentation of all possible result is mandatory
"""

import json
import os
import datetime
import jwt  # pylint: disable=import-error

from dotenv import load_dotenv

from ..db_helper import dbconn
from ..db_helper.errors import UniqueViolation
from ..general_helper.passwords import hash_password, is_hashed, verify_password
from ..general_helper.vec_rip import vec_rip
from ..general_helper.parse_user_info import parse_user_info

TOKEN_LIFETIME = datetime.timedelta(hours=1)
# Re-sign a token once it is within this window of expiring.
TOKEN_REFRESH_WINDOW = datetime.timedelta(minutes=15)
MIN_PASSWORD_LENGTH = 8


def _utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def normalize_email(email) -> str:
    """Emails are case-insensitive, so store and compare them folded."""
    return email.strip().lower() if isinstance(email, str) else email


class UserAuth:
    """
    Class for handling user authentication/creation.
    IS NOT an api endpoint, only parse info
    handles database
    should return a json for user info upon successful login/signup
    The status code is -1 when info is not provided properly
    SHOULD NOT HAPPEN if there is no bug.

    Naming convention: X_Y
    X: action such as login, signup, etc
    Y: method (or req abbrievation)
        go for google oauth
        e for email
        u for uid
        p for pwd
        n for user_name

    Returns a token in the response that is good for an hour
    """

    def __init__(self, database: dbconn.DBConn, args: dict = None) -> None:
        """
        takes in perspective info in the form of a json with varying fields depending on actions.
        Not having a field for an action will result in failure.
        """
        self.database = database
        self.args = args

    def sign_jwt(self, uid: str) -> str:
        """
        Signs a jwt token for the user
        Uses the auth secret from the env
        Includes the uid in the token

        Assume: auth is successful
        """
        load_dotenv()
        authsecret = os.getenv("JWT_REAUTH_SECRET")
        if not isinstance(authsecret, str) or not authsecret.strip():
            raise RuntimeError(
                "JWT_REAUTH_SECRET is not set. Copy .env.example to .env and set it, "
                "or run ./scripts/setup.sh."
            )
        return jwt.encode(
            {
                "uid": uid,
                "exp": _utcnow() + TOKEN_LIFETIME,
            },
            authsecret,
            algorithm="HS256",
        )

    def update_args(self, args: dict) -> None:
        """
        updates the args for the class
        """
        self.args = args

    def login_jwt(self, quick: bool = False) -> tuple[dict, int]:
        """
        logs in the user with a jwt token
        Requires uid, reauth_jwt
        """
        if not self.args["uid"] or not self.args["reauth_jwt"]:
            print("ERROR: uid or reauth_jwt not provided")
            return {"status": False, "detail": "no jwt/uid provided"}, 401
        load_dotenv()
        authsecret = os.getenv("JWT_REAUTH_SECRET")
        try:
            payload = jwt.decode(
                self.args["reauth_jwt"], authsecret, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            print("ERROR: jwt token expired")
            return {"status": False, "detail": "jwt token expired"}, 401
        except jwt.InvalidTokenError:
            print("ERROR: jwt token invalid")
            return {"status": False, "detail": "jwt token invalid"}, 401
        if payload["uid"] != self.args["uid"]:
            print(f"ERROR: uid mismatch (provided: {self.args['uid']}, token: {payload['uid']})")
            return {"status": False, "detail": "uid mismatch"}, 401
        if quick:
            return {"status": True, "detail": "jwt token valid"}, 200
        table_1 = self.database.run_sql(
            "SELECT * FROM data WHERE uid = %s;", (self.args["uid"],)
        )
        if not table_1:
            return {"status": False, "detail": {"status": "reauth failed, result bad"}}, 400
        expires_at = payload.get("exp")
        if expires_at is not None and _utcnow() <= datetime.datetime.fromtimestamp(
            expires_at, tz=datetime.timezone.utc
        ) - TOKEN_REFRESH_WINDOW:
            reduced_table = vec_rip(table_1[0])
            reduced_table.pop("pwd", None)
            parsed_info = parse_user_info(reduced_table)
            # Still comfortably valid, so hand the same token back.
            return {
                "status": True,
                "detail": reduced_table,
                "user_status": parsed_info,
                "jwt": self.args["reauth_jwt"],
            }, 200
        reduced_table = vec_rip(table_1[0])
        reduced_table.pop("pwd", None)
        parsed_info = parse_user_info(reduced_table)
        return {
            "status": True,
            "detail": reduced_table,
            "jwt": self.sign_jwt(self.args["uid"]),
            "user_status": parsed_info,
        }, 200
        # Successful auth returns a new jwt token with more valid time

    def login_up(self) -> tuple[dict, int]:
        """
        logs in the user with a username and password
        success code start with

        The remaining tuple is the api_ready response

        Expected result: success; user not found; wrongly authed; wrong password
        """
        if not self.args["uid"] or not self.args["pwd"]:
            # uid and pwd are mandatory
            print("ERROR: uid or pwd not provided")
            return {}, -1
        table_1 = self.database.run_sql(
            "SELECT * FROM data WHERE uid = %s;", (self.args["uid"],)
        )
        if not table_1:
            return {"status": False, "detail": {"status": "user not found"}}, 400
        if table_1[0]["auth_type"] != "eup":
            print("ERROR: auth type mismatch")
            return {"status": False, "detail": {"status": "auth type mismatch"}}, 401
        if verify_password(self.args["pwd"], table_1[0]["pwd"]):
            if not is_hashed(table_1[0]["pwd"]):
                # Upgrade a legacy plaintext row now that we know the password.
                self.database.run_sql(
                    "UPDATE data SET pwd = %s WHERE uid = %s",
                    (hash_password(self.args["pwd"]), self.args["uid"]),
                )
            reduced_table = vec_rip(table_1[0])
            reduced_table.pop("pwd", None)
            parsed_info = parse_user_info(reduced_table)
            return {
                "status": True,
                "detail": reduced_table,
                "user_status": parsed_info,
                "jwt": self.sign_jwt(self.args["uid"]),
            }, 200

        return {"status": False, "detail": {"status": "password incorrect"}}, 401

    def signup_eupn(self) -> tuple[dict, int]:
        """
        signs up the user with email, uid, password (and name)

        Expected result: success; uid unique violation
        """
        required_fields = ["uid", "pwd", "email", "user_name"]
        if any(not self.args[field] for field in required_fields):
            print("ERROR: uid, pwd, email, or name not provided")
            return {}, -1
        if len(self.args["pwd"]) < MIN_PASSWORD_LENGTH:
            return {
                "status": False,
                "detail": {
                    "status": f"password must be at least {MIN_PASSWORD_LENGTH} characters"
                },
            }, 400
        if "@" not in normalize_email(self.args["email"]):
            return {
                "status": False,
                "detail": {"status": "email address is not valid"},
            }, 400
        sql_query = """
            INSERT INTO data (uid, user_name, pwd, email, auth_type, userinfo, resumeinfo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.args["uid"],
            self.args["user_name"],
            hash_password(self.args["pwd"]),
            normalize_email(self.args["email"]),
            "eup",
            json.dumps({"email_verified": False}),
            json.dumps({}),
        )
        try:
            self.database.run_sql(sql_query, params)
            user_status = parse_user_info({})
            return {
                "status": True,
                "detail": {"status": "user created"},
                "jwt": self.sign_jwt(self.args["uid"]),
                "user_status": user_status,
            }, 201
        except UniqueViolation:
            print("UID unique violation")
            return {
                "status": False,
                "detail": {"status": "uid or email unique violation"},
            }, 409

    def delete_eup(self) -> tuple[dict, int]:
        """
        delete user with email, uid, password (and name)
        TO BE MIGRATED TO admin_user_edit.py
        Expected result: success; deletion failed (return specific error)
        """
        required_fields = ["uid", "pwd", "email"]
        if any(field not in self.args for field in required_fields):
            print("ERROR: uid, pwd, email, or name not provided")
            return {}, -1
        rows = self.database.run_sql(
            "SELECT pwd, email FROM data WHERE uid = %s AND auth_type = 'eup';",
            (self.args["uid"],),
        )
        if (
            not rows
            or rows[0]["email"] != normalize_email(self.args["email"])
            or not verify_password(self.args["pwd"], rows[0]["pwd"])
        ):
            return {
                "status": False,
                "detail": {"status": "credentials do not match"},
            }, 401
        try:
            self.database.run_sql(
                "DELETE FROM data WHERE uid = %s AND auth_type = 'eup';",
                (self.args["uid"],),
            )
            return {"status": True, "detail": {"status": "user deleted"}}, 200
        except Exception as e:  # pylint: disable=broad-except
            print(f"ERROR: {e}")
            return {
                "status": False,
                "detail": {"status": False, "detail": str(e)},
            }, 500

    def auth_go(self) -> tuple[dict, int]:
        """
        logs in the user with google oauth
        success code start with
        The remaining tuple is the api_ready response

        Expected result: success login; success signup; wrongly authed (upon login)
        """
        if not self.args["sub"]:
            print("ERROR: sub not provided")
            return {}, -1
        table_1 = self.database.run_sql(
            "SELECT * FROM data WHERE uid = %s;", (self.args["sub"],)
        )

        if not table_1:
            sql_query = """
                INSERT INTO data (uid, user_name, pwd, email, auth_type, userinfo, resumeinfo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.args["sub"],
                self.args["name"],
                "",
                normalize_email(self.args["email"]),
                "go",
                json.dumps({"email_verified": True}),
                json.dumps({}),
            )
            try:
                self.database.run_sql(sql_query, params)
                user_status = parse_user_info({})
                return {
                    "status": True,
                    "detail": {"message": "user created"},
                    "jwt": self.sign_jwt(self.args["sub"]),
                    "user_status": user_status,
                }, 201
            except UniqueViolation:
                print("BACKEND ERROR: on creation while account exists")
                return {}, -1
        if table_1[0]["auth_type"] != "go":
            return {"status": False, "message": "auth type mismatch"}, 401
        reduced_table = vec_rip(table_1[0])
        reduced_table.pop("pwd", None)
        parsed_info = parse_user_info(reduced_table)
        return {
            "status": True,
            "info": reduced_table,
            "jwt": self.sign_jwt(table_1[0]["uid"]),
            "user_status": parsed_info,
        }, 200

    def delete_go(self) -> tuple[dict, int]:
        """
        delete user with google oauth
        Expected result: success; deletion failed (return specific error)
        """
        if not self.args["uid"]:
            print("ERROR: sub not provided")
            return {}, -1
        sql_query = "DELETE FROM data WHERE uid = %s AND auth_type = 'go';"
        try:
            self.database.run_sql(sql_query, (self.args["uid"],))
            return {"status": True, "message": "user deleted"}, 200
        except Exception as e:  # pylint: disable=broad-except
            print(f"ERROR: {e}")
            return {
                "status": False,
                "message": f"deletion failed: {str(e)}",
            }, 400
