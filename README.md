# ResuMix

**Live Application:** [https://resu-mix.vercel.app/](https://resu-mix.vercel.app/)

A sentence-transformer-based AI-powered resume optimizer that generates job-specific, tailored resumes in seconds. Set your master resume once, then automatically generate perfectly optimized resumes for each job application.

---

## What is ResuMix?

ResuMix is an intelligent resume optimization platform that uses advanced AI and natural language processing to help job seekers create highly targeted resumes. Instead of manually tailoring your resume for each job application, ResuMix:

1. **Stores your master resume** - Enter all your experiences, skills, and achievements once
2. **Analyzes job descriptions** - Uses sentence transformers to understand job requirements
3. **Optimizes content** - Intelligently selects and ranks your most relevant experiences
4. **Generates PDFs** - Creates professional LaTeX-formatted resumes ready to submit

---

## Key Features

### AI-Powered Optimization
- **Sentence Transformer Scoring**: Uses the `all-mpnet-base-v2` model to compute semantic similarity between your resume content and job requirements
- **Multi-Category Analysis**: Evaluates content across technical skills, soft skills, and relevance
- **Smart Line Ranking**: Each line in your resume is scored and ranked based on job fit

### Master Resume Management
- **Structured Resume Builder**: Organize your resume into sections, items, and lines
- **Multiple Item Styles**: Support for various resume formats (2-4 heading styles, paragraphs)
- **LaTeX Export**: Professional PDF generation using PyLaTeX
- **Parameter Customization**: Fine-tune weights and biases for different content categories

### Secure Authentication
- **Multiple Auth Methods**: Email/password and Google OAuth integration
- **JWT-Based Sessions**: Secure reauthentication tokens for quick access
- **PostgreSQL Storage**: Secure user data and resume information storage

### Modern User Interface
- **React + Vite Frontend**: Fast, responsive single-page application
- **Intuitive Dashboard**: Track resume status, tweak parameters, and generate optimized resumes
- **Real-time Feedback**: Terminal-style output during resume generation
- **Wiki & Documentation**: Built-in help system

---

## Technical Architecture

### Frontend
- **Framework**: React 19 with Vite
- **Routing**: React Router DOM
- **State Management**: Context API for authentication
- **UI Components**: Custom component library with Lucide icons
- **API Communication**: Axios with credential support

### Backend
- **Framework**: Flask with Flask-RESTful
- **Language**: Python 3.x
- **API Type**: REST API
- **CORS**: Configured for cross-origin requests from Vercel deployments

### Database
- **Type**: PostgreSQL
- **Connection**: psycopg3 with connection pooling
- **Schema**: Single `data` table storing user info and resume data as JSONB

```sql
CREATE TABLE data (
    uid VARCHAR(256) PRIMARY KEY,
    user_name VARCHAR(64),
    pwd VARCHAR(64),
    email VARCHAR(256) NOT NULL UNIQUE,
    auth_type VARCHAR(16),
    userinfo JSONB,
    resumeInfo JSONB
);
```

### AI/ML Components
- **Sentence Transformers**: `all-mpnet-base-v2` for semantic similarity
- **OpenAI Integration**: GPT-4o-mini for parsing job requirements and generating structured data
- **Vector Embeddings**: Cached embeddings for efficient resume line scoring
- **Optimization Algorithm**: Custom scoring and shuffling algorithm for content selection

---

## Tech Stack

### Backend Dependencies
- **Flask** (3.1.1) - Web framework
- **sentence-transformers** (4.1.0) - Semantic similarity
- **PyLaTeX** (1.4.2) - PDF resume generation
- **PyJWT** (2.10.1) - Authentication tokens
- **psycopg** (3.2.3) - PostgreSQL database driver
- **openai** (1.82.0) - AI integration
- **torch** (2.7.1) - Deep learning framework
- **transformers** (4.52.4) - NLP models

### Frontend Dependencies
- **react** (19.1.0) - UI framework
- **react-router-dom** (6.30.1) - Routing
- **axios** (1.10.0) - HTTP client
- **@react-oauth/google** (0.12.2) - Google authentication
- **jwt-decode** (4.0.0) - JWT handling
- **lucide-react** (0.522.0) - Icons

---

## How It Works

### 1. User Registration & Authentication
Users can sign up using email/password or Google OAuth. Authentication tokens are stored securely using JWT.

### 2. Master Resume Creation
Users build their comprehensive master resume by:
- Adding sections (Education, Experience, Projects, Skills, etc.)
- Creating items within sections (jobs, degrees, projects)
- Writing lines for each item (bullet points, descriptions)
- Setting parameters (category weights and biases)

### 3. Job Description Analysis
When generating an optimized resume:
1. User pastes a job description
2. GPT-4o-mini extracts 3-12 core requirements
3. Requirements are converted to vector embeddings
4. Each resume line is scored against requirements using cosine similarity

### 4. Optimization & Selection
The optimization algorithm:
1. Scores each line (0-10 scale) based on semantic similarity
2. Applies category weights and biases
3. Selects the most relevant content for each section
4. Generates multiple versions and shuffles for optimal layout

### 5. PDF Generation
- Selected content is formatted using LaTeX templates
- PyLaTeX generates a professional PDF
- User downloads the tailored resume

---

## Data Structure

### Resume Hierarchy
```
ResumeInfo
├── sections (list)
│   ├── Section
│   │   ├── title (LaTeX string)
│   │   ├── items (list)
│   │   │   ├── Item
│   │   │   │   ├── titles (list of LaTeX strings)
│   │   │   │   ├── lines (list)
│   │   │   │   │   ├── Line
│   │   │   │   │   │   ├── content (LaTeX string)
│   │   │   │   │   │   ├── content_str (plain string)
│   │   │   │   │   │   ├── score (float 0-10)
│   │   │   │   │   │   ├── keywords (list)
│   │   │   │   │   │   └── aux_info (cached vectors)
│   │   │   │   ├── category_weight (dict)
│   │   │   │   └── category_bias (dict)
│   │   └── aux_info
└── heading_info (name, contact info)
```

---

## API Endpoints

### User Authentication
- `POST /user` - Sign up new user
- `GET /user` - Login with credentials or Google OAuth
- `PUT /user` - Update user information

### Resume Management
- `GET /resume` - Retrieve user's resume data
- `POST /resume` - Update resume information
- `PUT /resume` - Modify resume parameters

### Resume Generation
- `POST /resume/optimize` - Generate optimized PDF resume
- `POST /api/generate-resume` - Alternative PDF generation endpoint

---

## Use Cases

1. **Job Seekers**: Generate tailored resumes for multiple job applications
2. **Career Changers**: Emphasize different skills for different industries
3. **Recent Graduates**: Optimize limited experience for various roles
4. **Professionals**: Maintain one master resume, generate role-specific versions

---

## Security Features

- Password hashing for email/password authentication
- JWT tokens with expiration for session management
- Environment variable management for API keys
- CORS configuration for secure cross-origin requests
- PostgreSQL with parameterized queries to prevent SQL injection

---

## Future Enhancements

- Multiple resume templates and styles
- ATS (Applicant Tracking System) optimization
- Cover letter generation
- Interview preparation based on job requirements
- Analytics on which experiences perform best
- Multi-language support

---

## Contributing

This project is actively maintained. For questions or contributions, please refer to the project repository.

---

## License

See repository for license information.

---

## Acknowledgments

- Sentence Transformers library by UKPLab
- OpenAI GPT models
- PyLaTeX for PDF generation
- The open-source community

---

Built to help you land your dream job faster.



RULE:
- usually, make means to parse the information and to get the thing ready to be built
- build would be to build the object.


UPDATE: 
scoring is done only once with the master scoring function to enable functions such as:
- balancing skills
- preference of variety or depth