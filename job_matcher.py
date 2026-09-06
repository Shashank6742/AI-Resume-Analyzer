import pandas as pd
from skill_extractor import get_all_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles(file_path="data/job_roles.csv"):
    """Load job roles and required skills from CSV."""
    return pd.read_csv(file_path)


def calculate_match_score(resume_text, required_skills):
    """
    Calculate similarity between resume skills and required job skills
    using TF-IDF and cosine similarity.
    """

    documents = [resume_text, required_skills]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    return round(similarity * 100, 2)


def match_resume_to_roles(resume_text, job_roles):
    """
    Match a resume to job roles using only job-related skills.
    Personal attributes do not affect the matching score.
    """

    resume_skills = get_all_skills(resume_text)
    skill_text = " ".join(resume_skills)

    results = []

    for _, row in job_roles.iterrows():
        role = row["role"]
        required_skills = row["required_skills"]

        score = calculate_match_score(
            skill_text,
            required_skills
        )

        results.append({
            "role": role,
            "match_score": score
        })

    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results


def get_top_roles(results, number=3):
    """Return the top recommended job roles."""
    return results[:number]