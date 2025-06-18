"""
testing the item builder
"""

from ..resume_objects.resume import Resume
from ..resume_objects.latex_templates import LTemplate


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
            "title": "Experience",
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
                            "content": r"\item Developed feature X that improved performance by 30\%",
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
                            "content": r"\item Led a team of 5 engineers",
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
optimization_result = [
    # Section 0: we keep item 0 at version 2, and item 1 at version 0
    [
        [0, 0, 1],
        [0, 1, 0],
    ],
    # Section 1: we keep only item 0 at version 1
    [
        [1, 0, 1],
    ],
    # Section 2: no items fit, so an empty list
    [],
]
my_resume.optimization_result = optimization_result
resume_pdf = my_resume.build()
with open("test_resume.pdf", "wb") as f:
    f.write(resume_pdf)
print("Wrote test_resume.pdf")
