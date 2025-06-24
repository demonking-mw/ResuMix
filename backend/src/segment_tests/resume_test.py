"""
testing the item builder
"""

from ..resume_objects.resume import Resume
from ..resume_objects.latex_templates import LTemplate
from ..resume_objects.implementations.scoring_functions import simple_sum_function
import datetime

test_resume_dict = {
    "aux_info": {"type": "resume"},
    "heading_info": {
        "heading_name": "Marven Wang",
        "subsequent_content": [
            "m574wang@uwaterloo.ca",
            "647-705-3579",
            "github.com/m574wang",
        ],
    },
    "sections": [
        {
            "sect_id": 0,
            "aux_info": {"type": "section"},
            "title": "SKILLS",
            "items": [
                # original 3 items…
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Python, C, C\#, Java, Racket, Typescript, CSS, SQL; React JS, REST API, Flask, TensorFlow, Git",
                            "content_str": "Python, C, C#, Java, Racket, Typescript, CSS, SQL; React JS, REST API, Flask, TensorFlow, Git",
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Wix Studio, Unity, React JS, Tailwind, Flask, TensorFlow, GitHub Actions",
                            "content_str": "Wix Studio, Unity, React JS, Tailwind, Flask, TensorFlow, GitHub Actions",
                            "cate_score": {
                                "technical": {
                                    "Wix Studio": 3,
                                    "Unity": 3,
                                    "React JS": 2,
                                    "Tailwind": 2,
                                    "Flask": 2,
                                    "TensorFlow": 2,
                                    "GitHub Actions": 2,
                                },
                                "soft": {"learning": 1},
                                "relevance": {"devops": 1},
                            },
                            "keywords": ["devops"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"MySQL, PostgreSQL, MongoDB, SQLite, Redis, Cassandra",
                            "content_str": "MySQL, PostgreSQL, MongoDB, SQLite, Redis, Cassandra",
                            "cate_score": {
                                "technical": {
                                    "MySQL": 3,
                                    "PostgreSQL": 3,
                                    "MongoDB": 2,
                                    "SQLite": 2,
                                    "Redis": 2,
                                    "Cassandra": 1,
                                },
                                "soft": {"reliability": 1},
                                "relevance": {"data_storage": 1},
                            },
                            "keywords": ["data_storage"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                # --- newly added SKILLS items (3 more) ---
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Docker, Kubernetes, AWS, Azure, GCP",
                            "content_str": "Docker, Kubernetes, AWS, Azure, GCP",
                            "cate_score": {
                                "technical": {
                                    "Docker": 3,
                                    "Kubernetes": 3,
                                    "AWS": 3,
                                    "Azure": 2,
                                    "GCP": 2,
                                },
                                "soft": {"adaptability": 1},
                                "relevance": {"cloud_platforms": 1},
                            },
                            "keywords": ["cloud_platforms"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Selenium, PyTest, Jest, Mocha, Chai",
                            "content_str": "Selenium, PyTest, Jest, Mocha, Chai",
                            "cate_score": {
                                "technical": {
                                    "Selenium": 3,
                                    "PyTest": 2,
                                    "Jest": 2,
                                    "Mocha": 2,
                                    "Chai": 1,
                                },
                                "soft": {"attention_to_detail": 1},
                                "relevance": {"testing_tools": 1},
                            },
                            "keywords": ["testing_tools"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Git, GitHub, GitLab, Bitbucket, CI/CD pipelines",
                            "content_str": "Git, GitHub, GitLab, Bitbucket, CI/CD pipelines",
                            "cate_score": {
                                "technical": {
                                    "Git": 3,
                                    "GitHub": 2,
                                    "GitLab": 2,
                                    "Bitbucket": 1,
                                    "CI/CD": 2,
                                },
                                "soft": {"collaboration": 1},
                                "relevance": {"version_control": 1},
                            },
                            "keywords": ["version_control"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
        {
            "sect_id": 1,
            "aux_info": {"type": "section"},
            "title": "WORK EXPERIENCE",
            "items": [
                # original 2 items…
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Software Development Assistant",
                        "Apex Snow Academy",
                        "Apr. 2024–Aug. 2024",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented the company\'s website using Wix Studio, JavaScript, and CSS, attracted 200+ customer enrollments",
                            "content_str": "Implemented the company's website using Wix Studio, JavaScript, and CSS, attracted 200+ customer enrollments",
                            "cate_score": {
                                "technical": {
                                    "Wix Studio": 3,
                                    "JavaScript": 3,
                                    "CSS": 3,
                                    "web development": 2,
                                },
                                "soft": {"initiative": 2, "problem_solving": 2},
                                "relevance": {"customer_engagement": 1},
                            },
                            "keywords": ["customer_engagement"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Single-handedly built the backend of the student-matching system using Python and TensorFlow, achieved a 20\% increase in lesson hours and 13\% reduction in scheduling overflow",
                            "content_str": "Single-handedly built the backend of the student-matching system using Python and TensorFlow, achieved a 20% increase in lesson hours and 13% reduction in scheduling overflow",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "TensorFlow": 3,
                                    "backend development": 2,
                                },
                                "soft": {"initiative": 2, "innovation": 2},
                                "relevance": {"scheduling_optimization": 1},
                            },
                            "keywords": ["scheduling_optimization"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Optimized website performance, improving load times by 30\% through code splitting and image compression",
                            "content_str": "Optimized website performance, improving load times by 30% through code splitting and image compression",
                            "cate_score": {
                                "technical": {
                                    "performance optimization": 3,
                                    "code splitting": 2,
                                    "image compression": 2,
                                },
                                "soft": {"efficiency": 2},
                                "relevance": {"performance": 1},
                            },
                            "keywords": ["performance"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Collaborated with UX designers to refine UI/UX, increasing user engagement by 15\%",
                            "content_str": "Collaborated with UX designers to refine UI/UX, increasing user engagement by 15%",
                            "cate_score": {
                                "technical": {"UI/UX": 2, "collaboration": 2},
                                "soft": {"teamwork": 2},
                                "relevance": {"user_experience": 1},
                            },
                            "keywords": ["user_experience"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Software Development Intern",
                        "Akare Tech",
                        "Mar. 2023–Aug. 2023",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Developed a car-recognition and 3D scene reconstruction software using C\# and Python",
                            "content_str": "Developed a car-recognition and 3D scene reconstruction software using C# and Python",
                            "cate_score": {
                                "technical": {
                                    "C#": 3,
                                    "Python": 3,
                                    "computer vision": 2,
                                    "3D reconstruction": 2,
                                },
                                "soft": {"problem_solving": 2},
                                "relevance": {"computer_vision": 1},
                            },
                            "keywords": ["computer_vision"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Single-handedly developed a 3D scene visualizer with Unity, incorporating features such as auto scene switch and blacklist vehicle alert",
                            "content_str": "Single-handedly developed a 3D scene visualizer with Unity, incorporating features such as auto scene switch and blacklist vehicle alert",
                            "cate_score": {
                                "technical": {"Unity": 3, "C#": 2, "visualization": 2},
                                "soft": {"initiative": 2},
                                "relevance": {"visualization": 1},
                            },
                            "keywords": ["visualization"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed and trained the car recognition model, a CNN built with Python, reaching an overall test set accuracy of 93\%",
                            "content_str": "Designed and trained the car recognition model, a CNN built with Python, reaching an overall test set accuracy of 93%",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "CNN": 3,
                                    "model training": 2,
                                },
                                "soft": {"analysis": 2},
                                "relevance": {"model_accuracy": 1},
                            },
                            "keywords": ["model_accuracy"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Integrated the 3D reconstruction model into the security workflow, reducing manual checks by 25\%",
                            "content_str": "Integrated the 3D reconstruction model into the security workflow, reducing manual checks by 25%",
                            "cate_score": {
                                "technical": {"integration": 3, "automation": 2},
                                "soft": {"efficiency": 2},
                                "relevance": {"workflow_optimization": 1},
                            },
                            "keywords": ["workflow_optimization"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Wrote unit and integration tests covering 90\% of the codebase for the car-recognition system",
                            "content_str": "Wrote unit and integration tests covering 90% of the codebase for the car-recognition system",
                            "cate_score": {
                                "technical": {"test automation": 3, "unit testing": 2},
                                "soft": {"attention_to_detail": 2},
                                "relevance": {"quality_assurance": 1},
                            },
                            "keywords": ["quality_assurance"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Authored technical documentation and delivered training sessions to QA team on software operation",
                            "content_str": "Authored technical documentation and delivered training sessions to QA team on software operation",
                            "cate_score": {
                                "technical": {"documentation": 2},
                                "soft": {"communication": 2, "training": 2},
                                "relevance": {"knowledge_transfer": 1},
                            },
                            "keywords": ["knowledge_transfer"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                # --- newly added WORK EXPERIENCE items (2 more) ---
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Freelance Developer",
                        "Personal Projects",
                        "Jun. 2023–Dec. 2023",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built multiple client websites using React, Flask, and Firebase; delivered 5+ projects on time",
                            "content_str": "Built multiple client websites using React, Flask, and Firebase; delivered 5+ projects on time",
                            "cate_score": {
                                "technical": {
                                    "React": 3,
                                    "Flask": 2,
                                    "Firebase": 2,
                                },
                                "soft": {"time_management": 2},
                                "relevance": {"client_delivery": 1},
                            },
                            "keywords": ["client_delivery"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented user analytics dashboards and A/B tests, boosting user retention by 18\%",
                            "content_str": "Implemented user analytics dashboards and A/B tests, boosting user retention by 18%",
                            "cate_score": {
                                "technical": {
                                    "data visualization": 2,
                                    "A/B testing": 2,
                                },
                                "soft": {"analysis": 2},
                                "relevance": {"user_retention": 1},
                            },
                            "keywords": ["user_retention"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Teaching Assistant",
                        "University of Waterloo",
                        "Jan. 2025–Present",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Assist in grading assignments and leading discussion sections for Distributed Systems course (100+ students)",
                            "content_str": "Assist in grading assignments and leading discussion sections for Distributed Systems course (100+ students)",
                            "cate_score": {
                                "technical": {"distributed systems": 3},
                                "soft": {"mentoring": 2, "organization": 2},
                                "relevance": {"teaching": 1},
                            },
                            "keywords": ["teaching"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Hold weekly office hours to support student debugging and conceptual questions",
                            "content_str": "Hold weekly office hours to support student debugging and conceptual questions",
                            "cate_score": {
                                "technical": {"troubleshooting": 2},
                                "soft": {"communication": 2},
                                "relevance": {"student_support": 1},
                            },
                            "keywords": ["student_support"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
        {
            "sect_id": 2,
            "aux_info": {"type": "section"},
            "title": "PROJECTS & ACTIVITIES",
            "items": [
                # original 5 items…
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Pet Optimizer",
                        "International Mathematical Modelling Challenge",
                        "Apr. 2024",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led a team of 4 to develop a solution for the pet adoption situation across Canada for IMMC",
                            "content_str": "Led a team of 4 to develop a solution for the pet adoption situation across Canada for IMMC",
                            "cate_score": {
                                "technical": {"modeling": 3},
                                "soft": {"leadership": 2, "teamwork": 2},
                                "relevance": {"collaboration": 1},
                            },
                            "keywords": ["collaboration"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Programmed an adoption recommendation engine in Python using a neural network with 91\% test accuracy",
                            "content_str": "Programmed an adoption recommendation engine in Python using a neural network with 91% test accuracy",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "neural network": 3,
                                    "data science": 2,
                                },
                                "soft": {"innovation": 2},
                                "relevance": {"model_accuracy": 1},
                            },
                            "keywords": ["model_accuracy"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Received an honorable mention in the international round after winning the Canadian round",
                            "content_str": "Received an honorable mention in the international round after winning the Canadian round",
                            "cate_score": {
                                "technical": {"competition": 2},
                                "soft": {"achievement": 2},
                                "relevance": {"honorable_mention": 1},
                            },
                            "keywords": ["honorable_mention"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented cross-validation and hyperparameter tuning, improving recommendation precision by 8\%",
                            "content_str": "Implemented cross-validation and hyperparameter tuning, improving recommendation precision by 8%",
                            "cate_score": {
                                "technical": {
                                    "cross-validation": 3,
                                    "hyperparameter tuning": 2,
                                },
                                "soft": {"analysis": 2},
                                "relevance": {"precision_improvement": 1},
                            },
                            "keywords": ["precision_improvement"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Visualized model performance metrics in dashboards for stakeholder review",
                            "content_str": "Visualized model performance metrics in dashboards for stakeholder review",
                            "cate_score": {
                                "technical": {"data visualization": 3},
                                "soft": {"communication": 2},
                                "relevance": {"stakeholder_reporting": 1},
                            },
                            "keywords": ["stakeholder_reporting"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Co-authored project report and presented findings at university symposium",
                            "content_str": "Co-authored project report and presented findings at university symposium",
                            "cate_score": {
                                "technical": {"presentation": 2},
                                "soft": {"communication": 2},
                                "relevance": {"presentation": 1},
                            },
                            "keywords": ["presentation"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Everything Calendar",
                        "React JS, Tailwind",
                        "Oct. 2024–Present",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Developed a website using React JS and Tailwind to build custom calendars by scraping event sites",
                            "content_str": "Developed a website using React JS and Tailwind to build custom calendars by scraping event sites",
                            "cate_score": {
                                "technical": {
                                    "React JS": 3,
                                    "Tailwind": 2,
                                    "web scraping": 2,
                                },
                                "soft": {"initiative": 2},
                                "relevance": {"frontend_development": 1},
                            },
                            "keywords": ["frontend_development"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Planned, developed, and debugged the backend REST API in Python, optimized event scraping reliability",
                            "content_str": "Planned, developed, and debugged the backend REST API in Python, optimized event scraping reliability",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "REST API": 3,
                                    "backend development": 2,
                                },
                                "soft": {"problem_solving": 2},
                                "relevance": {"backend_development": 1},
                            },
                            "keywords": ["backend_development"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented user authentication and profile management with JWT in Flask",
                            "content_str": "Implemented user authentication and profile management with JWT in Flask",
                            "cate_score": {
                                "technical": {
                                    "Flask": 3,
                                    "JWT": 2,
                                    "authentication": 2,
                                },
                                "soft": {"security_awareness": 2},
                                "relevance": {"authentication": 1},
                            },
                            "keywords": ["authentication"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Set up CI/CD pipeline using GitHub Actions to automate testing and deployment",
                            "content_str": "Set up CI/CD pipeline using GitHub Actions to automate testing and deployment",
                            "cate_score": {
                                "technical": {"CI/CD": 3, "GitHub Actions": 2},
                                "soft": {"automation": 2},
                                "relevance": {"devops": 1},
                            },
                            "keywords": ["devops"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Grass Allergy Relief",
                        "Personal Project",
                        "Sept. 2024–Present",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Single-handedly built a resume tailoring application in Python, generating job-targeted resumes in under 10 seconds",
                            "content_str": "Single-handedly built a resume tailoring application in Python, generating job-targeted resumes in under 10 seconds",
                            "cate_score": {
                                "technical": {"Python": 3, "automation": 2},
                                "soft": {"initiative": 2},
                                "relevance": {"resume_automation": 1},
                            },
                            "keywords": ["resume_automation"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Automated personalized resume generation using a user-created database and job descriptions",
                            "content_str": "Automated personalized resume generation using a user-created database and job descriptions",
                            "cate_score": {
                                "technical": {"databases": 2, "automation": 2},
                                "soft": {"efficiency": 2},
                                "relevance": {"automation": 1},
                            },
                            "keywords": ["automation"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Conducted end-to-end testing, received over 20 positive feedbacks and multiple functionality reports",
                            "content_str": "Conducted end-to-end testing, received over 20 positive feedbacks and multiple functionality reports",
                            "cate_score": {
                                "technical": {"testing": 2},
                                "soft": {"attention_to_detail": 2},
                                "relevance": {"quality_assurance": 1},
                            },
                            "keywords": ["quality_assurance"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Deployed application as a Docker container, enabling one-click installation for end users",
                            "content_str": "Deployed application as a Docker container, enabling one-click installation for end users",
                            "cate_score": {
                                "technical": {"Docker": 3, "containerization": 2},
                                "soft": {"usability_focus": 2},
                                "relevance": {"deployment": 1},
                            },
                            "keywords": ["deployment"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Integrated logging and monitoring using Prometheus and Grafana to track usage metrics",
                            "content_str": "Integrated logging and monitoring using Prometheus and Grafana to track usage metrics",
                            "cate_score": {
                                "technical": {"Prometheus": 2, "Grafana": 2},
                                "soft": {"monitoring": 2},
                                "relevance": {"observability": 1},
                            },
                            "keywords": ["observability"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Conducted user interviews and iterated UI based on feedback, improving usability score by 20\%",
                            "content_str": "Conducted user interviews and iterated UI based on feedback, improving usability score by 20%",
                            "cate_score": {
                                "technical": {"UX research": 2},
                                "soft": {"user_research": 2},
                                "relevance": {"usability": 1},
                            },
                            "keywords": ["usability"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Drifting Engine", "C#, Unity", "Sept. 2024–Present"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Wrote a 2D drifting physics engine in C\# and Unity, developed a mini-game for testing",
                            "content_str": "Wrote a 2D drifting physics engine in C# and Unity, developed a mini-game for testing",
                            "cate_score": {
                                "technical": {
                                    "C#": 3,
                                    "Unity": 3,
                                    "physics simulation": 2,
                                },
                                "soft": {"creativity": 2},
                                "relevance": {"game_development": 1},
                            },
                            "keywords": ["game_development"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Modeled over/under steering, four-wheel drift, and other scenarios using data from personal research",
                            "content_str": "Modeled over/under steering, four-wheel drift, and other scenarios using data from personal research",
                            "cate_score": {
                                "technical": {"simulation": 3, "data analysis": 2},
                                "soft": {"analysis": 2},
                                "relevance": {"simulation": 1},
                            },
                            "keywords": ["simulation"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed and implemented a custom physics material system to simulate tire traction variations",
                            "content_str": "Designed and implemented a custom physics material system to simulate tire traction variations",
                            "cate_score": {
                                "technical": {"physics materials": 3},
                                "soft": {"innovation": 2},
                                "relevance": {"realism": 1},
                            },
                            "keywords": ["realism"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Optimized engine performance by refactoring core physics loops, increasing frame rate by 25\%",
                            "content_str": "Optimized engine performance by refactoring core physics loops, increasing frame rate by 25%",
                            "cate_score": {
                                "technical": {"performance optimization": 3},
                                "soft": {"efficiency": 2},
                                "relevance": {"performance": 1},
                            },
                            "keywords": ["performance"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Participant",
                        "Canadian National Physics Olympiad",
                        "May 2023",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Participated in the CPhO physics camp as one of the top 15 physics students in Canada",
                            "content_str": "Participated in the CPhO physics camp as one of the top 15 physics students in Canada",
                            "cate_score": {
                                "technical": {"physics": 3},
                                "soft": {"achievement": 2},
                                "relevance": {"competition": 1},
                            },
                            "keywords": ["competition"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Self-learned a first-year quantum physics course in 5 days for camp preparation",
                            "content_str": "Self-learned a first-year quantum physics course in 5 days for camp preparation",
                            "cate_score": {
                                "technical": {"quantum physics": 3},
                                "soft": {"self_learning": 2},
                                "relevance": {"quick_learning": 1},
                            },
                            "keywords": ["quick_learning"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Developed problem-solving and critical thinking abilities through laboratory design challenges and tests",
                            "content_str": "Developed problem-solving and critical thinking abilities through laboratory design challenges and tests",
                            "cate_score": {
                                "technical": {"laboratory research": 2},
                                "soft": {"problem_solving": 2, "critical_thinking": 2},
                                "relevance": {"skill_development": 1},
                            },
                            "keywords": ["skill_development"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Achieved top 10 score in the theoretical exam portion out of 100+ participants",
                            "content_str": "Achieved top 10 score in the theoretical exam portion out of 100+ participants",
                            "cate_score": {
                                "technical": {"exam_performance": 3},
                                "soft": {"achievement": 2},
                                "relevance": {"ranking": 1},
                            },
                            "keywords": ["ranking"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led peer study group focusing on classical mechanics and electromagnetism",
                            "content_str": "Led peer study group focusing on classical mechanics and electromagnetism",
                            "cate_score": {
                                "technical": {"mechanics": 2, "electromagnetism": 2},
                                "soft": {"leadership": 2},
                                "relevance": {"mentoring": 1},
                            },
                            "keywords": ["mentoring"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Published practice problem sets used by incoming camp attendees",
                            "content_str": "Published practice problem sets used by incoming camp attendees",
                            "cate_score": {
                                "technical": {"content creation": 2},
                                "soft": {"communication": 2},
                                "relevance": {"resource_development": 1},
                            },
                            "keywords": ["resource_development"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                # --- newly added PROJECTS & ACTIVITIES items (5 more) ---
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["ML Portfolio Tracker", "Python, Dash", "Jan. 2024"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built a stock portfolio tracking dashboard in Dash, supporting real-time price updates",
                            "content_str": "Built a stock portfolio tracking dashboard in Dash, supporting real-time price updates",
                            "cate_score": {
                                "technical": {"Dash": 3, "real-time data": 2},
                                "soft": {"initiative": 2},
                                "relevance": {"fintech": 1},
                            },
                            "keywords": ["fintech"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Implemented automated alerts via email and Slack when thresholds are breached",
                            "content_str": "Implemented automated alerts via email and Slack when thresholds are breached",
                            "cate_score": {
                                "technical": {"APIs": 2, "automation": 2},
                                "soft": {"communication": 2},
                                "relevance": {"alerting": 1},
                            },
                            "keywords": ["alerting"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Open-Source Contributor",
                        "Mozilla Foundation",
                        "2022–Present",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Contributed bug fixes and features to Firefox and Rust projects; merged 15+ PRs",
                            "content_str": "Contributed bug fixes and features to Firefox and Rust projects; merged 15+ PRs",
                            "cate_score": {
                                "technical": {"Rust": 3, "bug fixing": 3},
                                "soft": {"collaboration": 2},
                                "relevance": {"open source": 1},
                            },
                            "keywords": ["open source"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Authored documentation and migration guides for new contributors",
                            "content_str": "Authored documentation and migration guides for new contributors",
                            "cate_score": {
                                "technical": {"documentation": 2},
                                "soft": {"mentoring": 2},
                                "relevance": {"onboarding": 1},
                            },
                            "keywords": ["onboarding"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Personal Blog Platform", "Django, React", "2021"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built a full-stack blogging platform in Django with React front-end, featuring markdown support",
                            "content_str": "Built a full-stack blogging platform in Django with React front-end, featuring markdown support",
                            "cate_score": {
                                "technical": {
                                    "Django": 3,
                                    "React": 2,
                                    "API integration": 2,
                                },
                                "soft": {"detail_orientation": 2},
                                "relevance": {"content_management": 1},
                            },
                            "keywords": ["content_management"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Integrated social share APIs and implemented user authentication with JWT",
                            "content_str": "Integrated social share APIs and implemented user authentication with JWT",
                            "cate_score": {
                                "technical": {"APIs": 2, "authentication": 2},
                                "soft": {"security_awareness": 2},
                                "relevance": {"social_media": 1},
                            },
                            "keywords": ["social_media"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Volunteer Developer", "Local Nonprofit", "2020–2021"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built and maintained donation tracking portal using Flask and PostgreSQL",
                            "content_str": "Built and maintained donation tracking portal using Flask and PostgreSQL",
                            "cate_score": {
                                "technical": {"Flask": 3, "PostgreSQL": 2},
                                "soft": {"collaboration": 2},
                                "relevance": {"social_impact": 1},
                            },
                            "keywords": ["social_impact"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Trained staff on system use and generated weekly usage reports",
                            "content_str": "Trained staff on system use and generated weekly usage reports",
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Hackathon Winner", "Waterloo Hack", "Nov. 2019"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led a 3-person team to build an AI-powered chat app in 24 hours; won Best UX",
                            "content_str": "Led a 3-person team to build an AI-powered chat app in 24 hours; won Best UX",
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Presented demo to 200+ attendees and coordinated post-hack maintenance",
                            "content_str": "Presented demo to 200+ attendees and coordinated post-hack maintenance",
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
        {
            "sect_id": 3,
            "aux_info": {"type": "section"},
            "title": "EDUCATION",
            "items": [
                # original University item…
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "B.CS. Honours Computer Science",
                        "University of Waterloo",
                        "2024–2029",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Recipient of the Alumni Scholarship and the Presidential Scholarship of Distinction",
                            "content_str": "Recipient of the Alumni Scholarship and the Presidential Scholarship of Distinction",
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Relevant coursework: Algorithms, Data Structures, Operating Systems, Databases, Artificial Intelligence",
                            "content_str": "Relevant coursework: Algorithms, Data Structures, Operating Systems, Databases, Artificial Intelligence",
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                # --- newly added EDUCATION item (1 more) ---
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "High School Diploma",
                        "Waterloo Collegiate Institute",
                        "2016–2020",
                        "GPA: 3.9/4.0",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Graduated valedictorian; Captain of Math Team and Robotics Club",
                            "content_str": "Graduated valedictorian; Captain of Math Team and Robotics Club",
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Organized and led a weekly coding workshop for 50+ peers",
                            "content_str": "Organized and led a weekly coding workshop for 50+ peers",
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
    ],
}
template = LTemplate()
t0 = datetime.datetime.now()
my_resume = Resume(template, test_resume_dict)
if not my_resume.make(
    "This is a backend software engineer role, where the candidate will be instrumental in developing, hosting, and maintaining the robust server-side infrastructure and APIs on the cloud (AWS) that power our diverse applications. The candidate should have strong experience in backend development, especially with languages like Python (e.g., Django, Flask), Java (e.g., Spring Boot), or Node.js (e.g., Express). They should also be deeply familiar with designing and managing various databases (both relational like PostgreSQL or MySQL, and NoSQL like MongoDB or Redis) and possess a solid understanding of scalable architecture, API security, and distributed systems."
):
    print("sadge")
print("Resume made successfully")
print(my_resume.section_make_results)
my_resume.optimize()

print("Optimization result, here is the result:")
print(my_resume.optimization_result)
print("Building the resume PDF...")
resume_pdf = my_resume.build()
with open("test_resume.pdf", "wb") as f:
    f.write(resume_pdf)
print("Wrote test_resume.pdf")
t1 = datetime.datetime.now()
new_dict = my_resume.to_dict()

print("Just one more, once")
t2 = datetime.datetime.now()
my_resume2 = Resume(template, new_dict)
if not my_resume2.make(
    "We are seeking a passionate and skilled Frontend Dev Engineer to join our innovative product development team at [Your Company Name], where you'll be instrumental in bringing our user interfaces to life, ensuring they are visually stunning, highly performant, and a joy to use. In this role, you will design, develop, and maintain robust, scalable, and responsive user-facing features, collaborating closely with UI/UX designers to translate concepts into pixel-perfect applications and integrating seamlessly with backend APIs (RESTful and/or GraphQL); you'll also be responsible for optimizing performance, writing clean and testable code, participating in code reviews, and contributing to technical discussions and continuous process improvement. We're looking for someone with 3+ years of professional experience, possessing deep expertise in HTML5, CSS3, and modern JavaScript (ES6+), with strong proficiency in React.js and its ecosystem, extensive experience with TypeScript for building robust applications, and hands-on experience with state management libraries like Redux Toolkit. You should be familiar with modern styling solutions like Styled-Components or Tailwind CSS, adept at consuming APIs, and skilled in writing unit and integration tests using frameworks such as Jest and React Testing Library, all while proficiently using Git for version control. Our primary tech stack includes React.js, TypeScript, Redux Toolkit, and Styled-Components (with growing use of Tailwind CSS), all tested with Jest and React Testing Library, and built with Webpack (moving towards Vite); if you're excited by the opportunity to build exceptional user experiences, thrive in a collaborative environment, and work with a cutting-edge frontend stack, we encourage you to apply."
):
    print("sadge")
print("Resume made successfully")
my_resume2.optimize()

print("Optimization result, here is the result:")
print(my_resume2.optimization_result)
print("Building the resume PDF...")
resume_pdf2 = my_resume2.build()
with open("test_resume2.pdf", "wb") as f:
    f.write(resume_pdf2)
print("Wrote test_resume.pdf")
t3 = datetime.datetime.now()
print()
print(f"Time taken to make the first resume: {t1 - t0}")
print(f"Time taken to make the second resume: {t3 - t2}")
