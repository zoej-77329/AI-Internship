
SKILL_ALIASES = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ci/cd": "CI CD",
    "cicd": "CI CD",
    "tcp/ip": "TCP IP",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP"
}


def normalize_skill(skill):

    skill = str(skill).strip()

    if not skill:
        return ""

    return SKILL_ALIASES.get(
        skill.casefold(),
        skill.title()
    )


def normalize_skill_list(skills):

    normalized_skills = []

    for skill in skills:

        normalized = normalize_skill(skill)

        if normalized and normalized not in normalized_skills:
            normalized_skills.append(normalized)

    return normalized_skills

if __name__ == "__main__":

    skills = [
        "python",
        "PANDAS",
        "ml",
        "javascript",
        " python "
    ]

    print(normalize_skill_list(skills))