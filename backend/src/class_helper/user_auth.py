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
import psycopg  # type: ignore

from ..db_helper import dbconn
from ..general_helper.vec_rip import vec_rip
from ..general_helper.parse_user_info import parse_user_info


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
        if not isinstance(authsecret, str):
            raise TypeError("JWT_REAUTH_SECRET must be a string")
        return jwt.encode(
            {
                "uid": uid,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
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
            return {"status": False, "detail": "no jwt/uid provided"}, 401
        load_dotenv()
        authsecret = os.getenv("JWT_REAUTH_SECRET")
        try:
            payload = jwt.decode(
                self.args["reauth_jwt"], authsecret, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return {"status": False, "detail": "jwt token expired"}, 401
        except jwt.InvalidTokenError:
            return {"status": False, "detail": "jwt token invalid"}, 401
        if payload["uid"] != self.args["uid"]:
            return {"status": False, "detail": "uid mismatch"}, 401
        if quick:
            return {"status": True, "detail": "jwt token valid"}, 200
        sql_query = f"SELECT * FROM data WHERE uid = '{self.args['uid']}';"
        table_1 = self.database.run_sql(sql_query)
        if not table_1:
            return {"status": False, "detail": {"status": "reauth failed, result bad"}}, 400
        if datetime.datetime.utcnow() > datetime.datetime.fromtimestamp(
            payload["exp"]
        ) - datetime.timedelta(minutes=15):
            reduced_table = vec_rip(table_1[0])
            parsed_info = parse_user_info(reduced_table)
            print("Parsed info:", parsed_info)
            # Frequent resign prevention: will sign once every 20 min
            return {
                "status": True,
                "detail": reduced_table,
                "user_status": parsed_info,
                "jwt": self.sign_jwt(self.args["reauth_jwt"]),
            }, 200
        print("DEBUG: table for reauth", table_1)
        reduced_table = vec_rip(table_1[0])
        parsed_info = parse_user_info(reduced_table)
        print("Parsed info:", parsed_info)
        return {
            "status": True,
            "detail": reduced_table,
            "jwt": self.args["reauth_jwt"],
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
        sql_query = f"SELECT * FROM data WHERE uid = '{self.args['uid']}';"
        table_1 = self.database.run_sql(sql_query)
        if not table_1:
            return {"status": False, "detail": {"status": "user not found"}}, 400
        if table_1[0]["auth_type"] != "eup":
            return {"status": False, "detail": {"status": "auth type mismatch"}}, 401
        if table_1[0]["pwd"] == self.args["pwd"]:
            reduced_table = vec_rip(table_1[0])
            parsed_info = parse_user_info(reduced_table)
            print("Parsed info:", parsed_info)
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
        sql_query = """
            INSERT INTO data (uid, user_name, pwd, email, auth_type, userinfo, resumeinfo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self.args["uid"],
            self.args["user_name"],
            self.args["pwd"],
            self.args["email"],
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
        except psycopg.errors.UniqueViolation:
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
        sql_query = f"DELETE FROM data WHERE uid = '{self.args['uid']}' AND pwd = '{self.args['pwd']}' AND email = '{self.args['email']}';"
        try:
            self.database.run_sql(sql_query)
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
        sql_query = f"SELECT * FROM data WHERE uid = '{self.args['sub']}';"
        table_1 = self.database.run_sql(sql_query)

        if not table_1:
            sql_query = """
                INSERT INTO data (uid, user_name, pwd, email, auth_type, userinfo, resumeinfo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.args["sub"],
                self.args["name"],
                "",
                self.args["email"],
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
            except psycopg.errors.UniqueViolation:
                print("BACKEND ERROR: on creation while account exists")
                return {}, -1
        if table_1[0]["auth_type"] != "go":
            return {"status": False, "message": "auth type mismatch"}, 401
        reduced_table = vec_rip(table_1[0])
        parsed_info = parse_user_info(reduced_table)
        print("Parsed info:", parsed_info)
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
        sql_query = (
            f"DELETE FROM data WHERE uid = '{self.args['uid']}' AND auth_type = 'go';"
        )
        try:
            self.database.run_sql(sql_query)
            return {"status": True, "message": "user deleted"}, 200
        except Exception as e:  # pylint: disable=broad-except
            print(f"ERROR: {e}")
            return {
                "status": False,
                "message": f"deletion failed: {str(e)}",
            }, 400
