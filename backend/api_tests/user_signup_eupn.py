"""
user signup test
implement dropping in the future
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.post(
    BASE + "/user",
    json={
        "type": "eupn",
        "uid": "test2",
        "pwd": "monkey",
        "email": "fo0obar@lol.com",
        "user_name": "marmoset",
    },
    timeout=35,
)
print(response.json())
token = response.json().get("jwt")
if not response.json().get("status"):
    print("get failed")
    print(response.json())
    sys.exit(3)
response = requests.delete(
    BASE + "/user",
    json={
        "type": "eup",
        "uid": "test2",
        "pwd": "monkey",
        "email": "fo0obar@lol.com",
        "reauth_jwt": token,
    },
    timeout=35,
)
if not response.json().get("status"):
    print("delete failed")
    print(response.json())
    sys.exit(3)
print("delete success")
exit(0)
