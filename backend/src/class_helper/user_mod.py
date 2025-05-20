"""
Helper to modify any user data fields
    - uid: CANNOT BE MODIFIED, required for all
    - user_name
    - pwd: old pwd or email auth reqd
    - email: CANNOT BE MODIFIED
    - type: CANNOT BE MODIFIED
    - userinfo: modified by giving new dict
    - resumeinfo: modified by giving new dict
    Usage: provide a dict with fields to be modified and their values.
    Note: empty values will be ignored.
    For password change, provide old_pwd as an input.
    Note: there are no auth check on whether the field should be modified
    MUST NOT expose the entirety of this to frontend
    ALSO, WHETHER THE USER IS LOGGED IN OR NOT IS NOT CHECKED
    - this is a helper class, not a standalone class
"""

from ..db_helper import dbconn
from .user_auth import UserAuth
from ...general_helper import batch_ins_gen as big


class UserMod:
    """
    Usage: first create the object with args and db as input
    modifiable: user_name, pwd, userinfo, resumeinfo
    """

    def __init__(self, args: dict, db: dbconn.DBConn, email_auth: bool = False):
        self.args = args
        if "uid" in self.args and self.args["uid"] is not None:
            self.uid = self.args["uid"]
        else:
            self.uid = None
        if "uid" in self.args:
            del self.args["uid"]
        self.database = db
        self.email_auth = email_auth
        self.targets = {}
        self.executed = False
        if "pwd" in self.args and self.args["pwd"] is not None:
            if "old_pwd" in self.args and self.__old_pwd_check():
                self.targets["pwd"] = self.args["pwd"]
            elif (
                "email" in self.args
                and self.args["email"] is not None
                and self.email_auth
            ):
                self.targets["pwd"] = self.args["pwd"]
        if "user_name" in self.args and self.args["user_name"] is not None:
            self.targets["user_name"] = self.args["user_name"]
        if "userinfo" in self.args and isinstance(self.args["userinfo"], dict):
            self.targets["userinfo"] = self.args["userinfo"]
        if "resumeinfo" in self.args and isinstance(self.args["resumeinfo"], dict):
            self.targets["resumeinfo"] = self.args["resumeinfo"]

    def __old_pwd_check(self) -> bool:
        """
        check if the old password is correct
        """
        newargs = {"uid": self.uid, "pwd": self.args["old_pwd"]}
        auth_obj = UserAuth(self.database, newargs)
        _, login_status = auth_obj.login_up()
        if login_status == 200:
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        Override the default class print statement to provide a summary of the object.
        """
        if self.executed:
            return f"UserMod({', '.join(self.targets.keys())}) - EXECUTED"
        return f"UserMod({', '.join(self.targets.keys())})"

    def modify(self) -> bool:
        if not self.uid:
            print("ERROR: uid not provided")
            return False

        upd_query, values = big.create_query(
            "data",
            self.targets,
            "uid",
            self.args["uid"],
        )
        self.database.run_sql(upd_query, values)
        return True
