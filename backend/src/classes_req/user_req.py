"""
input requirments for user class

Requirement naming rule:
lowercase_with_underscore

Commenting: ALL_CAP for required, lowercase for optional
"""

from flask_restful import reqparse

# User Auth: TYPE, jwt_token, reauth_jwt, action, email, uid, pwd, user_name
# THIS IS FOR LOGIN
#################################################################
user_auth = reqparse.RequestParser()
user_auth.add_argument(
    "type",
    type=str,
    help="Type is required, can be email, up, or go",
    required=True,
)
user_auth.add_argument(
    "jwt_token", type=str, help="JWT token for go type", required=False, default=None
)
user_auth.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=False,
    default=None,
)
user_auth.add_argument("email", type=str, help="Email", required=False)
user_auth.add_argument("uid", type=str, help="User ID", required=False)
user_auth.add_argument("pwd", type=str, help="Password", required=False)