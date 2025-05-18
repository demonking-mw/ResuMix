"""
tests login with sample
"""

import sys
import requests

BASE = "http://127.0.0.1:5000"

response = requests.get(
    BASE + "/user",
    json={"type": "up", "uid": "test", "pwd": "monkey"},
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
