"""
Basic operations for user auth, info access/modification
Let's try relative input this time
dbconn rule:
- Define it here
- Toss it around to helpers
- Helpers that takes dbconn as input has no responsibility to close it
- Usually, dbconns are closed here. MUST DOCUMENT OTHERWISE CASES.

"""

# pylint: disable=import-error
from flask_restful import Resource
from ...src.db_helper.dbconn import DBConn
from ...src.classes_req import user_req
from ...src.class_helper import user_auth
from ...src.general_helper.google_auth_extract import GoogleAuthExtract as gae


class User(Resource):
    """
    CLASS USAGE:

    """

    def get(self) -> tuple[dict, int]:
        """
        Gets all user info after authentication
        Creates a new user if not exists and having enough info (go type)
        Note: SIGN IN ONLY
        """
        args = user_req.user_auth.parse_args()
        # Check auth type
        if args["type"] == "email":
            # NOT BUILT YET
            # REQUIRING EMAIL AUTH METHOD
            return {"status": False, "message": "Email auth not implemented"}, 501
        elif args["type"] == "up":
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            user_auth_json, login_status = user_auth_obj.login_up()
            database.close()
            if login_status == -1:  # Login_status SHOULD be defined if this is reached
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            else:
                return user_auth_json, login_status
        elif args["type"] == "go":
            if args["jwt_token"] is None:
                return {
                    "status": False,
                    "message": "JWT token is required for go auth type",
                }, 400
            auth_jwt = gae(args["jwt_token"])
            if not auth_jwt.authenticate():
                return {"status": False, "message": "go auth failed, bad jwt"}, 401
            # JWT token authed at this point
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, auth_jwt.decoded)
            user_auth_json, login_status = user_auth_obj.auth_go()
            database.close()
            if login_status == -1:
                print("ERROR: something is cooked for login")
                return {"status": False, "message": "info incomplete or defect"}, 400
            else:
                return user_auth_json, login_status
        else:
            return {"status": False, "message": "Invalid auth type"}, 400
