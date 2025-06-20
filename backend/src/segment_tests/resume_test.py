"""
testing the item builder
"""

from ..resume_objects.resume import Resume
from ..resume_objects.latex_templates import LTemplate
from ..resume_objects.implementations.scoring_functions import simple_sum_function


test_resume_dict = {
    "aux_info": {"type": "resume"},
    "heading_info": {
        "heading_name": "John Doe",
        "subsequent_content": ["Software Engineer", "john.doe@example.com", "555-1234"],
    },
    "sections": [
        {
            # this will be passed as sect_id to Section(...)
            "sect_id": 0,
            "aux_info": {"type": "section"},
            "title": "EXPERIENCE",
            "items": [
                {
                    # aux_info must include type "items" and a style (here 'l' = bullet list)
                    "aux_info": {"type": "items", "style": "l"},
                    # these will become the four arguments to \resumeSubheading
                    "titles": [
                        "Software Engineer",
                        "ACME Corp",
                        "2019 – 2021",
                        "New York, NY",
                    ],
                    # each line dict must declare type "lines"; content is the raw LaTeX,
                    # content_str the plain-text fallback, and we can start with empty scores
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Developed feature 'random skibidi shinanigan' that improved performance by 69% and resulted in a 100 percent increase in monkey production. Let's just say that this line is really long and takes up multiple lines",
                            "content_str": "Developed feature X that improved performance by 30%",
                            "cate_score": {
                                "technical": {},
                                "soft": {},
                                "relevance": {},
                            },
                            "keywords": [],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led a team of 5 engineers",
                            "content_str": "Led a team of 5 engineers",
                            "cate_score": {
                                "technical": {},
                                "soft": {},
                                "relevance": {},
                            },
                            "keywords": [],
                        },
                    ],
                    # cate_scores is used by Item.__init__ when style != 'p'
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 1.0},
                        "soft": {"weight": 1.0, "bias": 1.0},
                        "relevance": {"weight": 1.0, "bias": 1.0},
                    },
                }
            ],
        }
    ],
}

template = LTemplate()

my_resume = Resume(template, test_resume_dict)
my_resume.make(
    "This is a typical backend software engineer role requiring Python, SQL, and team leadership skills. "
)
print("Resume made successfully")
my_resume.optimize(simple_sum_function)
print("Optimization result, here is the result:")
print(my_resume.optimization_result)
print("Building the resume PDF...")
resume_pdf = my_resume.build()
with open("test_resume.pdf", "wb") as f:
    f.write(resume_pdf)
print("Wrote test_resume.pdf")


val = {
    "technical": {
        "scores": {
            "problem_solving": 2.0,
            "team_management": 0,
            "project_management": 0,
            "performance_improvement": 3.0,
            "communication": 0,
            "feature_development": 3.0,
            "leadership": 0,
            "software_engineering": 2.0,
        },
        "bias": 1.0,
    },
    "soft": {
        "scores": {
            "problem_solving": 2.0,
            "teamwork": 0,
            "communication": 1.0,
            "leadership": 0,
        },
        "bias": 1.0,
    },
    "relevance": {"scores": {"interest": 1.0, "passion": 1.0}, "bias": 1.0},
}
