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
from ...src.classes_req.user_req import user_req
from ...rc.general_helper.google_auth_extract import GoogleAuthExtract as gae


class User(Resource):
    """
    CLASS USAGE:
    
    """
    def get(self):
        """
        Gets all user info after authentication
        Creates a new user if not exists and having enough info (go type)
        """
        args = user_req.user_auth.parse_args()
        # Check auth type
        if args["type"] == "email":
            pass
        elif args["type"] == "up":
            pass
        elif args["type"] == "go":
            if args["jwt_token"] is None:
                return {"status": False, "message": "JWT token is required for go auth type"}, 400
            auth_jwt = gae(args["jwt_token"])
            if not auth_jwt.authenticate():
                return {"status": False, "message": "go auth failed, bad jwt"}, 401
            # JWT token authed at this point
            database = DBConn()
            # INSERT USER AUTH FUNCTION HERE
            database.close()
        else:
            return {"status": False, "message": "Invalid auth type"}, 400
    

