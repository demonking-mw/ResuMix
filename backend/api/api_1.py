# backend/api/api_1.py

"""
Hosting the API. Functionality is written elsewhere

Usage:
- Login: provided the proper info for go/up login
    - Will get a jwt token for easy reauth in the short future
-
"""

# pylint: disable=import-error
from flask import Flask, request, jsonify, send_file
from flask_restful import Api
from flask_cors import CORS
from .classes.user import User
from .classes.resume import ResumeHandle
from .classes.optimize import ResumeOptimizer

from io import BytesIO

# Import your resume-related modules
from backend.src.resume_objects.resume import Resume
from backend.src.resume_objects.latex_templates import LTemplate
from backend.src.resume_objects.implementations.scoring_functions import simple_sum_function


app = Flask(__name__)

# ---- MERGED CORS CONFIGURATION ----
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}},
    supports_credentials=True,
)

api = Api(app)

api.add_resource(User, "/user")
api.add_resource(ResumeHandle, "/resume")
api.add_resource(ResumeOptimizer, "/resume/optimize")
# api.add_resource(UserInfo, "/user/info")
# api.add_resource(Activity, "/activity")


@app.route("/api/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json()
    print("Received data:", data)

    resume_dict = data.get("resume_dict")
    job_description = data.get("job_description", "")

    if not resume_dict:
        print("Missing resume_dict")
        return jsonify({"error": "Missing resume_dict"}), 400

    template = LTemplate()
    my_resume = Resume(template, resume_dict)
    my_resume.make(job_description)
    my_resume.optimize(simple_sum_function)

    pdf_bytes = my_resume.build()
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resume.pdf",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
