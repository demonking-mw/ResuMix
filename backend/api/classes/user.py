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
from src.db_helper.dbconn import DBConn
from src.classes_req import user_req
from src.class_helper import user_auth
from src.general_helper.google_auth_extract import GoogleAuthExtract as gae


class User(Resource):
    """
    CLASS USAGE:

    """

    def __go_auth(self, args: dict) -> tuple[dict, int]:
        """
        Handles the go auth here because login and signup are identical
        """
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

        return user_auth_json, login_status

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
        if args["type"] == "up":
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            user_auth_json, login_status = user_auth_obj.login_up()
            database.close()
            if login_status == -1:  # Login_status SHOULD be defined if this is reached
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            return user_auth_json, login_status
        if args["type"] == "go":
            return self.__go_auth(args)

        return {"status": False, "message": "Invalid auth type"}, 400

    def post(self) -> tuple[dict, int]:
        """
        Creates a new user and log the user in
        """

        args = user_req.user_signup.parse_args()

        # Login via user/password
        if args["type"] == "up":
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            user_auth_json, login_status = user_auth_obj.login_up()
            database.close()
            if login_status == -1:
                # password mismatch
                return {"status": False, "detail": {"status": "info mismatch"}}, 400
            # returns {"status": True, "jwt": "...", ...}, 200
            return user_auth_json, login_status
        
        # Check auth type
        if args["type"] == "go":
            return self.__go_auth(args)
        if args["type"] == "eupn":
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            user_auth_json, login_status = user_auth_obj.signup_eupn()
            database.close()
            if login_status == -1:  # Login_status will be defined if this is reached
                print("ERROR: something is cooked for login")
                return {"status": False, "detail": {"status": "info mismatch"}}, 400

            return user_auth_json, login_status

        return {"status": False, "message": "Invalid auth type"}, 400

    def delete(self) -> tuple[dict, int]:
        """
        Delete the user
        FUTURE: keep the email tracked, maintain some basic info
        """
        args = user_req.user_delete.parse_args()
        if args["type"] == "go":
            if not args["jwt_token"]:
                return {
                    "status": False,
                    "message": "JWT token is required for go auth type",
                }, 400
            auth_jwt = gae(args["jwt_token"])
            if not auth_jwt.authenticate():
                return {"status": False, "message": "go auth failed, bad jwt"}, 401
            jwt_decode_uid = auth_jwt.decoded.get("sub")
            args["uid"] = jwt_decode_uid
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            reauth_result, login_status = user_auth_obj.login_jwt(quick=True)
            if login_status != 200:
                print("reauth result: ", reauth_result)
                database.close()
                return {
                    "status": False,
                    "detail": {"status": "Reauth failure, user not logged in"},
                }, 400
            user_auth_json, del_status = user_auth_obj.delete_go()
            database.close()
            return user_auth_json, del_status
        if args["type"] == "eup":
            req = ["email", "uid", "pwd"]
            if any(not args[field] for field in req):
                return {
                    "status": False,
                    "message": f"Missing required fields: {', '.join(req)}",
                }, 400
            database = DBConn()
            user_auth_obj = user_auth.UserAuth(database, args)
            reauth_result, login_status = user_auth_obj.login_jwt(quick=True)
            if login_status != 200:
                print("reauth result: ", reauth_result)
                return {
                    "status": False,
                    "detail": {"status": "Reauth failure, user not logged in"},
                }, 400
            user_auth_json, del_status = user_auth_obj.delete_eup()
            database.close()
            if del_status == -1:
                print("ERROR: something is cooked for deletion")
                return {
                    "status": False,
                    "detail": {"status": "internal error, should not happen"},
                }, 400
            else:
                return user_auth_json, del_status

        return {"status": False, "message": "Invalid auth type"}, 400
