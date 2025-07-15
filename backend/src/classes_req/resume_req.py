"""
input requirments for resume class

Requirement naming rule:
lowercase_with_underscore

Commenting: ALL_CAP for required, lowercase for optional
"""

from flask_restful import reqparse

# resume get (generate): JWT_TOKEN, set_cache, uid, pwd
#################################################################
resume_get = reqparse.RequestParser()
resume_get.add_argument(
    "uid",
    type=str,
    help="User ID to identify the user, required for resume generation",
    required=True,
)
resume_get.add_argument(
    "reauth_jwt",
    type=str,
    help="reauth_jwt to authenticate user",
    required=True,
)
resume_get.add_argument(
    "no_cache",
    type=bool,
    help="regenerate cache if this is set to true, will take some extra time",
    default=False,
)
resume_get.add_argument(
    "job_description",
    type=str,
    help="Job description used to generate resume",
    required=True,
)

resume_post = reqparse.RequestParser()
resume_post.add_argument(
    "uid",
    type=str,
    help="User ID to identify the user, required for resume update",
    required=True,
)
resume_post.add_argument(
    "reauth_jwt",
    type=str,
    help="reauth_jwt to authenticate user",
    required=True,
)
resume_post.add_argument(
    "resumeinfo",
    type=dict,
    help="Resume info to set, should be a dict",
    required=True,
)
