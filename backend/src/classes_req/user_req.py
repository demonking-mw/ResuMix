"""
input requirments for user class

Requirement naming rule:
lowercase_with_underscore

Commenting: ALL_CAP for required, lowercase for optional
"""

from flask_restful import reqparse

# Accept credentials from a JSON body (preferred) or the query string (legacy).
# Query strings end up in server logs and browser history, so clients should POST.
AUTH_LOCATIONS = ("json", "values")

# User Auth: TYPE, jwt_token, email, uid, pwd
# THIS IS FOR LOGIN
#################################################################
user_auth = reqparse.RequestParser()
user_auth.add_argument(
    "type",
    type=str,
    help="Type is required, can be email, up, or go or re",
    required=True,
    location=AUTH_LOCATIONS,
)
user_auth.add_argument(
    "jwt_token",
    type=str,
    help="JWT token for go type",
    required=False,
    default=None,
    location=AUTH_LOCATIONS,
)

user_auth.add_argument(
    "email", type=str, help="Email", required=False, location=AUTH_LOCATIONS
)
user_auth.add_argument(
    "uid", type=str, help="User ID", required=False, location=AUTH_LOCATIONS
)
user_auth.add_argument(
    "pwd", type=str, help="Password", required=False, location=AUTH_LOCATIONS
)
user_auth.add_argument(
    "reauth_jwt",
    type=str,
    help="Reauth JWT for re type",
    required=False,
    location=AUTH_LOCATIONS,
)


# User Sign Up: TYPE, jwt_token, email, uid, pwd, user_name
user_signup = reqparse.RequestParser()
user_signup.add_argument(
    "type",
    type=str,
    help="Type is required, can be email, up, or go",
    required=True,
)
user_signup.add_argument(
    "jwt_token", type=str, help="JWT token for go type", required=False, default=None
)
user_signup.add_argument("email", type=str, help="Email", required=False)
user_signup.add_argument("uid", type=str, help="User ID", required=False)
user_signup.add_argument("pwd", type=str, help="Password", required=False)
user_signup.add_argument(
    "user_name", type=str, help="User name", required=False, default=None
)
user_signup.add_argument(
    "reauth_jwt",
    type=str,
    help="Reauth JWT, used when type is 're'",
    required=False,
    default=None,
)


# User Delete: TYPE, jwt_token, REAUTH_JWT, email, uid, pwd
user_delete = reqparse.RequestParser()
user_delete.add_argument(
    "type",
    type=str,
    help="Type is required, can be email, up, or go",
    required=True,
)
user_delete.add_argument(
    "jwt_token", type=str, help="JWT token for go type", required=False, default=None
)
user_delete.add_argument(
    "reauth_jwt",
    type=str,
    help="Reauth JWT, required for deletion",
    required=True,
)
user_delete.add_argument("email", type=str, help="Email", required=False)
user_delete.add_argument("uid", type=str, help="User ID", required=False)
user_delete.add_argument("pwd", type=str, help="Password", required=False)
