import numpy as np
import os
from dotenv import load_dotenv

from ..resume_objects.line_eval import line_eval
from sentence_transformers import SentenceTransformer


# a minimal Line class for demo
class Line:
    def __init__(self, text):
        self.text = text
        self.score = None


reqs = [
    "Strong Python backend development.",
    "Experience building REST APIs.",
    "Familiarity with AWS deployments.",
]

lines = [
    Line("Built a frontend app in React."),
    Line("Developed RESTful APIs with Flask on AWS."),
    Line("Managed a Kubernetes cluster."),
]

ok = line_eval(reqs, lines)
if ok:
    for L in lines:
        print(f"{L.score:4.1f}  ←  {L.text}")
else:
    print("Scoring failed.")
