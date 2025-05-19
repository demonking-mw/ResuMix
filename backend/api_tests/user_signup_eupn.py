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
if response.json().get("status"):
    print("complete\n")
    print(response.json())
    sys.exit(0)
else:
    print("get failed")
    print(response.json())
    sys.exit(3)
