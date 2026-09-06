# AI Resume Analyzer & Job Recommendation System

## Project Overview

AI Resume Analyzer is a Streamlit-based application that analyzes resumes and provides career guidance based on job-related skills.

The system extracts resume text, identifies technical skills, compares them with predefined job roles, calculates match scores, identifies skill gaps, and generates a personalized learning roadmap.

## Features

- Upload resumes in PDF or DOCX format
- Extract and clean resume text
- Automatically detect technical and job-related skills
- Categorize detected skills
- Compare resume skills with multiple job roles
- Calculate job-role match scores using TF-IDF and cosine similarity
- Recommend the top 3 suitable career roles
- Analyze skill gaps for a selected target role
- Generate a personalized learning roadmap
- Interactive Streamlit dashboard
- Responsible AI approach focused on job-related skills

## Job Roles Supported

The system currently analyzes the resume against these roles:

- Data Analyst
- Machine Learning Engineer
- AI Engineer
- NLP Engineer
- Computer Vision Engineer
- Python Developer
- Data Scientist
- Full Stack Developer
- Cloud/DevOps Engineer
- AI/ML Intern

## Technology Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- PyPDF
- python-docx
- TF-IDF
- Cosine Similarity

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── sample_resumes/
├── reports/
└── tests/
    └── test_cases.csv
How It Works
Resume Upload
      ↓
Text Extraction
      ↓
Text Cleaning
      ↓
Skill Extraction
      ↓
Job Role Matching
      ↓
Match Score Calculation
      ↓
Top Career Recommendations
      ↓
Skill Gap Analysis
      ↓
Learning Roadmap
Installation
1. Clone the Repository
git clone <your-github-repository-url>
cd AI-Resume-Analyzer
2. Create Virtual Environment

For Windows:

python -m venv venv
3. Activate Virtual Environment

For Command Prompt:

venv\Scripts\activate
4. Install Required Packages
pip install -r requirements.txt
5. Run the Application
streamlit run app.py

The application will open in your browser.

Matching Method

The system uses TF-IDF vectorization and cosine similarity to compare resume-related skills with the skills required for each job role.

The matching process focuses on job-related skills so that unrelated personal attributes do not influence career recommendations.

Skill Gap Analysis

For a selected target role, the system compares the skills detected in the resume with the required skills for that role.

It displays:

Matched skills
Missing skills
Recommended learning topics
Personalized learning roadmap
Testing

The project was tested for:

PDF extraction
DOCX extraction
Unsupported file handling
Text cleaning
Skill extraction
Unrelated word filtering
Job-role matching
Top 3 recommendations
Score consistency
Skill-gap identification
Learning roadmap generation
Fairness with respect to personal attributes
Responsible AI

This application is intended for career guidance and learning recommendations. It is not designed for automatic hiring or candidate rejection.

The system focuses on job-related skills and does not use attributes such as gender, religion, nationality, or age for career matching.

Match scores are estimates and should not be treated as definitive measures of a candidate's ability.

Limitations
Skill extraction is primarily keyword-based.
Matching depends on the skills included in the job-role dataset.
A missing keyword does not necessarily mean the candidate lacks the actual ability.
Match scores are estimates rather than professional hiring decisions.
Future Improvements

Possible improvements include:

More comprehensive skill datasets
Improved semantic skill matching
Job description upload
More advanced NLP-based skill extraction
Expanded career-role database
Conclusion

AI Resume Analyzer provides an interactive way for users to understand their current skills, explore suitable career roles, identify skill gaps, and follow a structured learning roadmap.

The project demonstrates practical use of Python, NLP-style text processing, machine learning techniques, data processing, and Streamlit application development.