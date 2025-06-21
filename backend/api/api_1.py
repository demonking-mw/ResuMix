"""
Hosting the API. Functionality is written elsewhere
"""

# pylint: disable=import-error
from flask import Flask, request, jsonify, send_file
from flask_restful import Api
from flask_cors import CORS
from .classes.user import User

from io import BytesIO

from .classes.user import User

# Import your resume-related modules (adjust import paths as needed)
from ..src.resume_objects.resume import Resume
from ..src.resume_objects.latex_templates import LTemplate
from ..src.resume_objects.implementations.scoring_functions import simple_sum_function

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}},
    supports_credentials=True,
)
api = Api(app)

# @app.after_request
# def apply_cors_headers(response):
#     """Automatically add CORS headers to all responses"""
#     response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response


api.add_resource(User, "/user")
# api.add_resource(UserInfo, "/user/info")
# api.add_resource(Activity, "/activity")


@app.route("/api/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json()
    print("Received data:", data)  # <--- Add this

    resume_dict = data.get("resume_dict")
    job_description = data.get("job_description", "")

    if not resume_dict:
        print("Missing resume_dict")  # <--- Add this
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
        download_name="resume.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
