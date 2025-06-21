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
        "subsequent_content": [
            "Senior Software Engineer",
            "john.doe@example.com",
            "555-1234",
            "linkedin.com/in/johndoe",
            "github.com/johndoe",
        ],
    },
    "sections": [
        {
            "sect_id": 0,
            "aux_info": {"type": "section"},
            "title": "EXPERIENCE",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Senior Software Engineer",
                        "ACME Corp",
                        "2021 – Present",
                        "New York, NY",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Architected and implemented microservices using Python and Docker, reducing deployment time by 75\%.",
                            "content_str": "Architected and implemented microservices using Python and Docker, reducing deployment time by 75%.",
                            "cate_score": {
                                "technical": {
                                    "microservices": 3,
                                    "Python": 3,
                                    "Docker": 3,
                                    "deployment optimization": 2,
                                },
                                "soft": {
                                    "communication": 1,
                                    "problem_solving": 2,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led cross-functional teams of up to 8 engineers, sprinters and QA to deliver 5 major features per quarter.",
                            "content_str": "Led cross-functional teams of up to 8 engineers, sprinters and QA to deliver 5 major features per quarter.",
                            "cate_score": {
                                "technical": {
                                    "leadership": 3,
                                    "teamwork": 3,
                                    "project_management": 3,
                                    "communication": 2,
                                },
                                "soft": {
                                    "leadership": 3,
                                    "collaboration": 2,
                                },
                                "relevance": {
                                    "sprinters": 1,
                                    "led": 1,
                                },
                            },
                            "keywords": ["sprinters", "led"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Introduced CI/CD pipelines with Jenkins and GitHub Actions, improving release frequency by 300\%.",
                            "content_str": "Introduced CI/CD pipelines with Jenkins and GitHub Actions, improving release frequency by 300%.",
                            "cate_score": {
                                "technical": {
                                    "CI/CD": 3,
                                    "Jenkins": 3,
                                    "GitHub Actions": 3,
                                    "Release Management": 2,
                                },
                                "soft": {
                                    "communication": 2,
                                    "problem_solving": 3,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.2, "bias": 1.0},
                        "soft": {"weight": 1.0, "bias": 1.0},
                        "relevance": {"weight": 1.0, "bias": 1.0},
                    },
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Software Engineer",
                        "BetaCorp",
                        "2019 – 2021",
                        "San Francisco, CA",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed and built RESTful APIs in Node.js serving 2M+ daily active users.",
                            "content_str": "Designed and built RESTful APIs in Node.js serving 2M+ daily active users.",
                            "cate_score": {
                                "technical": {
                                    "RESTful APIs": 3,
                                    "Node.js": 3,
                                    "Scalability": 2,
                                    "Backend Development": 3,
                                },
                                "soft": {
                                    "communication": 2,
                                    "problem_solving": 3,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Optimized MySQL queries and Redis caching, cutting average response times from 350ms to 50ms.",
                            "content_str": "Optimized MySQL queries and Redis caching, cutting average response times from 350ms to 50ms.",
                            "cate_score": {
                                "technical": {
                                    "MySQL": 3,
                                    "Redis": 3,
                                    "Performance Optimization": 3,
                                    "Query Optimization": 3,
                                },
                                "soft": {
                                    "communication": 1,
                                    "problem_solving": 3,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 1.0},
                        "soft": {"weight": 0.8, "bias": 1.0},
                        "relevance": {"weight": 1.0, "bias": 1.0},
                    },
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Software Development Intern",
                        "Gamma Solutions",
                        "Summer 2018",
                        "Austin, TX",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented data visualization dashboards in React.js, increasing data visibility for stakeholders by 40\%.",
                            "content_str": "Implemented data visualization dashboards in React.js, increasing data visibility for stakeholders by 40%.",
                            "cate_score": {
                                "technical": {
                                    "React.js": 3,
                                    "Data Visualization": 3,
                                    "Stakeholder Communication": 2,
                                    "Performance Improvement": 2,
                                },
                                "soft": {
                                    "communication": 2,
                                    "problem_solving": 2,
                                },
                                "relevance": {
                                    "data visualization": 1,
                                    "React.js": 1,
                                },
                            },
                            "keywords": ["data visualization", "React.js"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 0.5},
                        "soft": {"weight": 1.0, "bias": 0.5},
                        "relevance": {"weight": 1.0, "bias": 0.5},
                    },
                },
            ],
        },
        {
            "sect_id": 1,
            "aux_info": {"type": "section"},
            "title": "EDUCATION",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "B.S. in Computer Science",
                        "MARMOSET!!!",
                        "State University",
                        "2015 – 2019",
                        "GPA: 3.8/4.0",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Relevant Coursework: Algorithms, Data Structures, Databases, Operating Systems, AI.",
                            "content_str": "Relevant Coursework: Algorithms, Data Structures, Databases, Operating Systems, AI.",
                            "cate_score": {
                                "technical": {
                                    "Algorithms": 3,
                                    "Data Structures": 3,
                                    "Databases": 2,
                                    "Operating Systems": 2,
                                },
                                "soft": {
                                    "problem_solving": 2,
                                    "critical_thinking": 2,
                                },
                                "relevance": {
                                    "Algorithms": 1,
                                    "AI": 1,
                                },
                            },
                            "keywords": ["Algorithms", "AI"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"President of Programming Club; organized hackathons with 200+ participants.",
                            "content_str": "President of Programming Club; organized hackathons with 200+ participants.",
                            "cate_score": {
                                "technical": {
                                    "leadership": 3,
                                    "event_organization": 3,
                                    "community_engagement": 2,
                                    "programming": 1,
                                },
                                "soft": {
                                    "leadership": 3,
                                    "organizational_skills": 3,
                                },
                                "relevance": {
                                    "hackathons": 1,
                                    "Programming Club": 1,
                                },
                            },
                            "keywords": ["hackathons", "Programming Club"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 0.8},
                        "soft": {"weight": 1.0, "bias": 0.8},
                        "relevance": {"weight": 0.5, "bias": 0.5},
                    },
                },
            ],
        },
        {
            "sect_id": 2,
            "aux_info": {"type": "section"},
            "title": "PROJECTS",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Real-Time Chat App", "React, Typescript", "2020"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built a WebSocket-based chat application in Go and Vue.js, supporting 1000 concurrent users.",
                            "content_str": "Built a WebSocket-based chat application in Go and Vue.js, supporting 1000 concurrent users.",
                            "cate_score": {
                                "technical": {
                                    "WebSocket": 3,
                                    "Go": 3,
                                    "Vue.js": 3,
                                    "Scalability": 2,
                                },
                                "soft": {
                                    "communication": 2,
                                    "problem_solving": 3,
                                },
                                "relevance": {
                                    "WebSocket": 1,
                                    "chat application": 1,
                                },
                            },
                            "keywords": ["WebSocket", "chat application"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Deployed on AWS with Terraform and Docker Compose.",
                            "content_str": "Deployed on AWS with Terraform and Docker Compose.",
                            "cate_score": {
                                "technical": {
                                    "AWS": 3,
                                    "Terraform": 3,
                                    "Docker": 3,
                                    "Deployment": 2,
                                },
                                "soft": {
                                    "communication": 1,
                                    "problem_solving": 2,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 0.5},
                        "soft": {"weight": 0.7, "bias": 0.5},
                        "relevance": {"weight": 0.5, "bias": 0.5},
                    },
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Machine Learning Pipeline",
                        "Kaggle Competition",
                        "2019",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed end-to-end ML pipeline in Python with scikit-learn, achieving top 5\% placement.",
                            "content_str": "Designed end-to-end ML pipeline in Python with scikit-learn, achieving top 5% placement.",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "Machine Learning": 3,
                                    "scikit-learn": 3,
                                    "Pipeline Design": 2,
                                },
                                "soft": {
                                    "problem_solving": 3,
                                    "technical_skills": 3,
                                },
                                "relevance": {
                                    "passion": 1,
                                    "interest": 1,
                                },
                            },
                            "keywords": ["passion", "interest"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.2, "bias": 0.5},
                        "soft": {"weight": 0.5, "bias": 0.5},
                        "relevance": {"weight": 0.5, "bias": 0.5},
                    },
                },
            ],
        },
        {
            "sect_id": 3,
            "aux_info": {"type": "section"},
            "title": "SKILLS",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "p"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"The humble onion is a global culinary cornerstone. Its pungent, sweet, and savory layers add versatile depth to countless dishes, from raw salads to caramelized bases. An indispensable kitchen staple, it's known for its flavor… and those infamous tear-jerking fumes. A small price for its kitchen dominance!",
                            "content_str": "The humble onion is a global culinary cornerstone. Its pungent, sweet, and savory layers add versatile depth to countless dishes, from raw salads to caramelized bases. An indispensable kitchen staple, it's known for its flavor… and those infamous tear-jerking fumes. A small price for its kitchen dominance!",
                            "cate_score": {
                                "technical": {
                                    "Algorithms": 3,
                                    "Data Structures": 3,
                                    "Databases": 2,
                                    "Operating Systems": 2,
                                },
                                "soft": {
                                    "problem_solving": 2,
                                    "critical_thinking": 2,
                                },
                                "relevance": {
                                    "Algorithms": 1,
                                    "AI": 1,
                                },
                            },
                            "keywords": ["Algorithms", "AI"],
                        },
                    ],
                    "cate_scores": {
                        "technical": {"weight": 1.0, "bias": 0.8},
                        "soft": {"weight": 1.0, "bias": 0.8},
                        "relevance": {"weight": 0.5, "bias": 0.5},
                    },
                },
            ],
        },
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
