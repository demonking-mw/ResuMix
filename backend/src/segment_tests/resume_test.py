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
                        "2021–Present",
                        "New York, NY",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Architected and implemented microservices in Python & Docker, slashing deployment time by 75\%.",
                            "content_str": "Architected and implemented microservices in Python & Docker, slashing deployment time by 75%.",
                            "cate_score": {
                                "technical": {
                                    "microservices": 3,
                                    "Python": 3,
                                    "Docker": 3,
                                    "deployment optimization": 2,
                                },
                                "soft": {"communication": 2, "problem_solving": 2},
                                "relevance": {"innovation": 1},
                            },
                            "keywords": ["innovation"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led a cross-functional team of 12 Engineers and QA to deliver 6 major features per quarter.",
                            "content_str": "Led a cross-functional team of 12 Engineers and QA to deliver 6 major features per quarter.",
                            "cate_score": {
                                "technical": {
                                    "leadership": 3,
                                    "teamwork": 3,
                                    "project_management": 3,
                                    "QA processes": 2,
                                },
                                "soft": {"leadership": 3, "collaboration": 2},
                                "relevance": {"mentorship": 1},
                            },
                            "keywords": ["mentorship"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Introduced CI/CD pipelines with Jenkins & GitHub Actions, boosting release cadence by 300\%.",
                            "content_str": "Introduced CI/CD pipelines with Jenkins & GitHub Actions, boosting release cadence by 300%.",
                            "cate_score": {
                                "technical": {
                                    "CI/CD": 3,
                                    "Jenkins": 3,
                                    "GitHub Actions": 3,
                                    "release engineering": 2,
                                },
                                "soft": {"initiative": 2, "problem_solving": 2},
                                "relevance": {"automation": 1},
                            },
                            "keywords": ["automation"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Software Engineer",
                        "BetaCorp",
                        "2019–2021",
                        "San Francisco, CA",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed & built RESTful APIs in Node.js serving 2M+ DAU with 99.9\% uptime.",
                            "content_str": "Designed & built RESTful APIs in Node.js serving 2M+ DAU with 99.9% uptime.",
                            "cate_score": {
                                "technical": {
                                    "RESTful APIs": 3,
                                    "Node.js": 3,
                                    "scalability": 2,
                                    "uptime engineering": 2,
                                },
                                "soft": {"communication": 2, "detail_orientation": 2},
                                "relevance": {"performance": 1},
                            },
                            "keywords": ["performance"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Optimized MySQL queries and Redis caching, cutting latencies from 350ms to 50ms.",
                            "content_str": "Optimized MySQL queries and Redis caching, cutting latencies from 350ms to 50ms.",
                            "cate_score": {
                                "technical": {
                                    "MySQL": 3,
                                    "Redis": 3,
                                    "query optimization": 3,
                                    "cache design": 2,
                                },
                                "soft": {"analysis": 2, "problem_solving": 3},
                                "relevance": {"efficiency": 1},
                            },
                            "keywords": ["efficiency"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Collaborated with frontend team to integrate GraphQL endpoints in React apps.",
                            "content_str": "Collaborated with frontend team to integrate GraphQL endpoints in React apps.",
                            "cate_score": {
                                "technical": {
                                    "GraphQL": 3,
                                    "React": 2,
                                    "API integration": 2,
                                },
                                "soft": {"teamwork": 2, "communication": 2},
                                "relevance": {"cross-functional": 1},
                            },
                            "keywords": ["cross-functional"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
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
                            "content": r"Built data-visualization dashboards in React.js, increasing stakeholder visibility by 40\%.",
                            "content_str": "Built data-visualization dashboards in React.js, increasing stakeholder visibility by 40%.",
                            "cate_score": {
                                "technical": {
                                    "React.js": 3,
                                    "data visualization": 3,
                                    "UX/UI collaboration": 2,
                                },
                                "soft": {"creativity": 2, "communication": 2},
                                "relevance": {"visual design": 1},
                            },
                            "keywords": ["visual design"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Automated end-to-end tests with Selenium, reducing regression bugs by 30\%.",
                            "content_str": "Automated end-to-end tests with Selenium, reducing regression bugs by 30%.",
                            "cate_score": {
                                "technical": {"Selenium": 3, "test automation": 3},
                                "soft": {
                                    "attention_to_detail": 2,
                                    "problem_solving": 2,
                                },
                                "relevance": {"quality_assurance": 1},
                            },
                            "keywords": ["quality_assurance"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Junior Developer",
                        "Delta Tech",
                        "2016–2018",
                        "Seattle, WA",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Maintained legacy Java codebase; refactored critical modules to Spring Boot.",
                            "content_str": "Maintained legacy Java codebase; refactored critical modules to Spring Boot.",
                            "cate_score": {
                                "technical": {
                                    "Java": 3,
                                    "Spring Boot": 3,
                                    "legacy systems": 2,
                                },
                                "soft": {"adaptability": 2, "analysis": 2},
                                "relevance": {"system_maintenance": 1},
                            },
                            "keywords": ["system_maintenance"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Integrated third-party payment gateway (Stripe) with internal services.",
                            "content_str": "Integrated third-party payment gateway (Stripe) with internal services.",
                            "cate_score": {
                                "technical": {"Stripe": 3, "API integration": 2},
                                "soft": {"collaboration": 2},
                                "relevance": {"e-commerce": 1},
                            },
                            "keywords": ["e-commerce"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Led weekly code reviews and mentored two new hires.",
                            "content_str": "Led weekly code reviews and mentored two new hires.",
                            "cate_score": {
                                "technical": {"code_review": 3},
                                "soft": {"mentoring": 3, "leadership": 2},
                                "relevance": {"team_growth": 1},
                            },
                            "keywords": ["team_growth"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Research Assistant",
                        "State University",
                        "2015–2016",
                        "College Town, USA",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built a distributed log-analysis tool in Go processing 10M events/day.",
                            "content_str": "Built a distributed log-analysis tool in Go processing 10M events/day.",
                            "cate_score": {
                                "technical": {
                                    "Go": 3,
                                    "distributed systems": 3,
                                    "log analysis": 2,
                                },
                                "soft": {"research": 2},
                                "relevance": {"data_pipelines": 1},
                            },
                            "keywords": ["data_pipelines"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Published findings in ACM symposium on large-scale system monitoring.",
                            "content_str": "Published findings in ACM symposium on large-scale system monitoring.",
                            "cate_score": {
                                "technical": {"academic writing": 2},
                                "soft": {"communication": 2},
                                "relevance": {"publication": 1},
                            },
                            "keywords": ["publication"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
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
                        "M.S. in Computer Science",
                        "Ivy University",
                        "2019–2021",
                        "GPA: 3.9/4.0",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Thesis: “Scalable Stream Processing in Kubernetes” supervised by Prof. X.",
                            "content_str": "Thesis: “Scalable Stream Processing in Kubernetes” supervised by Prof. X.",
                            "cate_score": {
                                "technical": {"stream processing": 3, "Kubernetes": 3},
                                "soft": {"research": 2},
                                "relevance": {"academic_interest": 1},
                            },
                            "keywords": ["academic_interest"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Graduate TA for Distributed Systems course (graded 200+ assignments).",
                            "content_str": "Graduate TA for Distributed Systems course (graded 200+ assignments).",
                            "cate_score": {
                                "technical": {"distributed systems": 3},
                                "soft": {"mentoring": 2, "organization": 2},
                                "relevance": {"teaching": 1},
                            },
                            "keywords": ["teaching"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "B.S. in Computer Science",
                        "State University",
                        "2011–2015",
                        "GPA: 3.8/4.0",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Relevant coursework: Algorithms, Data Structures, OS, DB, AI.",
                            "content_str": "Relevant coursework: Algorithms, Data Structures, OS, DB, AI.",
                            "cate_score": {
                                "technical": {
                                    "Algorithms": 3,
                                    "Data Structures": 3,
                                    "Operating Systems": 2,
                                    "Databases": 2,
                                    "AI": 2,
                                },
                                "soft": {"analysis": 2},
                                "relevance": {"academic_interest": 1},
                            },
                            "keywords": ["academic_interest"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"President, Programming Club: organized hackathons with 300+ participants.",
                            "content_str": "President, Programming Club: organized hackathons with 300+ participants.",
                            "cate_score": {
                                "technical": {"event_planning": 2},
                                "soft": {"leadership": 3, "organization": 2},
                                "relevance": {"community": 1},
                            },
                            "keywords": ["community"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
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
                    "titles": ["Real-Time Chat App", "Go, Vue.js", "2020"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built WebSocket chat server in Go, supporting 10k+ concurrent users.",
                            "content_str": "Built WebSocket chat server in Go, supporting 10k+ concurrent users.",
                            "cate_score": {
                                "technical": {
                                    "WebSocket": 3,
                                    "Go": 3,
                                    "concurrency": 2,
                                },
                                "soft": {"initiative": 2},
                                "relevance": {"real-time systems": 1},
                            },
                            "keywords": ["real-time systems"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Deployed via Docker Compose on AWS EC2, automated with Terraform.",
                            "content_str": "Deployed via Docker Compose on AWS EC2, automated with Terraform.",
                            "cate_score": {
                                "technical": {"Docker": 3, "AWS": 3, "Terraform": 3},
                                "soft": {"operations": 2},
                                "relevance": {"infrastructure": 1},
                            },
                            "keywords": ["infrastructure"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["ML Pipeline", "Kaggle Competition", "2019"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built end-to-end ML pipeline in Python with scikit-learn; top 5\% finish.",
                            "content_str": "Built end-to-end ML pipeline in Python with scikit-learn; top 5% finish.",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "scikit-learn": 3,
                                    "ML pipeline": 2,
                                },
                                "soft": {"problem_solving": 3},
                                "relevance": {"data science": 1},
                            },
                            "keywords": ["data science"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Distributed Logging System", "Open Source", "2018"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Authored an open-source log aggregator in Rust, 1k+ GitHub stars.",
                            "content_str": "Authored an open-source log aggregator in Rust, 1k+ GitHub stars.",
                            "cate_score": {
                                "technical": {
                                    "Rust": 3,
                                    "open source": 2,
                                    "log aggregation": 2,
                                },
                                "soft": {"community": 1},
                                "relevance": {"OSS contribution": 1},
                            },
                            "keywords": ["OSS contribution"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Automated Testing Framework", "Personal", "2017"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Designed a plug-in based test framework in Python, used by 50+ devs.",
                            "content_str": "Designed a plug-in based test framework in Python, used by 50+ devs.",
                            "cate_score": {
                                "technical": {"Python": 3, "test frameworks": 3},
                                "soft": {"automation": 2},
                                "relevance": {"developer tools": 1},
                            },
                            "keywords": ["developer tools"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Personal Blog Platform", "Django, React", "2016"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Built full-stack blogging platform in Django with React front-end.",
                            "content_str": "Built full-stack blogging platform in Django with React front-end.",
                            "cate_score": {
                                "technical": {"Django": 3, "React": 3, "full stack": 2},
                                "soft": {"initiative": 2},
                                "relevance": {"content management": 1},
                            },
                            "keywords": ["content management"],
                        },
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Integrated markdown editor and social share APIs.",
                            "content_str": "Integrated markdown editor and social share APIs.",
                            "cate_score": {
                                "technical": {"Markdown": 2, "API integration": 2},
                                "soft": {"problem_solving": 2},
                                "relevance": {"social media": 1},
                            },
                            "keywords": ["social media"],
                        },
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
        {
            "sect_id": 3,
            "aux_info": {"type": "section"},
            "title": "SKILLS",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Python, Go, Java, C\+\+, JavaScript, Rust",
                            "content_str": "Python, Go, Java, C++, JavaScript, Rust",
                            "cate_score": {
                                "technical": {
                                    "Python": 3,
                                    "Go": 3,
                                    "Java": 3,
                                    "C++": 2,
                                    "JavaScript": 3,
                                    "Rust": 2,
                                },
                                "soft": {"adaptability": 1},
                                "relevance": {"polyglot": 1},
                            },
                            "keywords": ["polyglot"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Frameworks & Tools", "test"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Docker, Kubernetes, AWS, Jenkins, Terraform, React, Vue",
                            "content_str": "Docker, Kubernetes, AWS, Jenkins, Terraform, React, Vue",
                            "cate_score": {
                                "technical": {
                                    "Docker": 3,
                                    "Kubernetes": 3,
                                    "AWS": 3,
                                    "Jenkins": 2,
                                    "Terraform": 2,
                                    "React": 2,
                                    "Vue": 2,
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
                    "titles": ["Databases", "test"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"PostgreSQL, MySQL, MongoDB, Redis, Cassandra",
                            "content_str": "PostgreSQL, MySQL, MongoDB, Redis, Cassandra",
                            "cate_score": {
                                "technical": {
                                    "PostgreSQL": 3,
                                    "MySQL": 3,
                                    "MongoDB": 2,
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
            ],
        },
        # (Sections 4–8: Certifications, Honors, Volunteer, Publications, Interests)
        # these have no "lines" or already have no lines so they won’t trigger AI
        {
            "sect_id": 4,
            "aux_info": {"type": "section"},
            "title": "VOLUNTEER",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Coding Mentor", "Girls Who Code", "2017–Present"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Mentored 50+ high-school students in Python & web development.",
                            "content_str": "Mentored 50+ high-school students in Python & web development.",
                            "cate_score": {
                                "technical": {"Python": 2, "web development": 2},
                                "soft": {"mentoring": 3, "communication": 2},
                                "relevance": {"community outreach": 1},
                            },
                            "keywords": ["community outreach"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": [
                        "Open-Source Contributor",
                        "Mozilla Foundation",
                        "2016–Present",
                    ],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Contributed patches to Firefox & Rust projects; fixed 20+ bugs.",
                            "content_str": "Contributed patches to Firefox & Rust projects; fixed 20+ bugs.",
                            "cate_score": {
                                "technical": {"Rust": 2, "bug fixing": 3},
                                "soft": {"collaboration": 2},
                                "relevance": {"open source": 1},
                            },
                            "keywords": ["open source"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                },
            ],
        },
        {
            "sect_id": 5,
            "aux_info": {"type": "section"},
            "title": "INTERESTS",
            "items": [
                {
                    "aux_info": {"type": "items", "style": "n"},
                    "titles": ["Interests", "tests"],
                    "lines": [
                        {
                            "aux_info": {"type": "lines"},
                            "content": r"Hiking, gourmet cooking, open-source hacking, and AI ethics reading groups.",
                            "content_str": "Hiking, gourmet cooking, open-source hacking, and AI ethics reading groups.",
                            "cate_score": {
                                "technical": {"python": 0},
                                "soft": {"curiosity": 2, "creativity": 2},
                                "relevance": {
                                    "hiking": 1,
                                    "cooking": 1,
                                    "hacking": 1,
                                    "AI ethics": 1,
                                },
                            },
                            "keywords": ["hiking", "cooking", "hacking", "AI ethics"],
                        }
                    ],
                    "cate_scores": {"weight": 1.0, "bias": 0.0},
                }
            ],
        },
    ],
}


template = LTemplate()

my_resume = Resume(template, test_resume_dict)
if not my_resume.make(
    "This is a typical backend software engineer role requiring Python, SQL, and team leadership skills. "
):
    print("sadge")
print("Resume made successfully")
print(my_resume.section_make_results)
my_resume.optimize(simple_sum_function)

print("Optimization result, here is the result:")
print(my_resume.optimization_result)
print("Building the resume PDF...")
resume_pdf = my_resume.build()
with open("test_resume.pdf", "wb") as f:
    f.write(resume_pdf)
print("Wrote test_resume.pdf")
