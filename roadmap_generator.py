def get_skill_gap(resume_skills, required_skills):
    """
    Compare resume skills with the skills required for a job role.
    """

    resume_skills = {skill.lower().strip() for skill in resume_skills}
    required_skills = {
        skill.lower().strip()
        for skill in required_skills
    }

    matched_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills - resume_skills
    )

    return matched_skills, missing_skills


def generate_roadmap(missing_skills):
    """
    Generate a simple learning roadmap based on missing skills.
    """

    roadmap = []

    if not missing_skills:
        return [
            {
                "week": "Ready",
                "topic": "All required skills detected",
                "goal": "Continue building projects and practical experience."
            }
        ]

    # Divide missing skills into groups of approximately 2 per week
    for index in range(0, len(missing_skills), 2):

        week_number = (index // 2) + 1

        skills = missing_skills[index:index + 2]

        roadmap.append({
            "week": f"Week {week_number}",
            "topic": ", ".join(skill.title() for skill in skills),
            "goal": f"Learn the fundamentals and complete a small practical task using {', '.join(skills)}."
        })

    return roadmap