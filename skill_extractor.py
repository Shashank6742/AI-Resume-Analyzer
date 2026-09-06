import re


SKILL_CATEGORIES = {
    "Programming": [
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "html",
        "css"
    ],

    "Data & Databases": [
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "excel",
        "pandas",
        "numpy"
    ],

    "AI & Machine Learning": [
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "nlp",
        "computer vision",
        "transformers",
        "hugging face",
        "llm",
        "rag"
    ],

    "Web & APIs": [
        "fastapi",
        "flask",
        "django",
        "rest api",
        "api"
    ],

    "Cloud & DevOps": [
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "google cloud",
        "git",
        "github"
    ],

    "Tools & Visualization": [
        "power bi",
        "tableau",
        "matplotlib",
        "plotly",
        "streamlit",
        "linux"
    ]
}


def extract_skills(text):
    """
    Extract recognized skills from resume text.
    """

    text = text.lower()

    found_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills[category] = []

        for skill in skills:

            # Match the complete skill phrase
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, text):
                found_skills[category].append(skill)

    return found_skills


def get_all_skills(text):
    """
    Return all detected skills as a single list.
    """

    categorized_skills = extract_skills(text)

    all_skills = []

    for skills in categorized_skills.values():
        all_skills.extend(skills)

    return sorted(set(all_skills))