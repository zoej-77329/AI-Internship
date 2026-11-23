from data_loader import load_career_skills


def analyze_skill_gap(user_skills, career_goal):

    careers = load_career_skills()

    career = careers[
        careers["career_goal"].str.lower() == career_goal.lower()
    ]

    if career.empty:
        print("Career goal not found.")
        return None

    required_skills = set(career.iloc[0]["required_skills"])
    current_skills = set(user_skills)

    matched_skills = current_skills.intersection(required_skills)
    missing_skills = required_skills - current_skills

    coverage = (
        len(matched_skills) / len(required_skills) * 100
        if required_skills else 100
    )

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage": coverage
    }


if __name__ == "__main__":

    user_skills = ["Python", "Pandas"]

    result = analyze_skill_gap(user_skills, "AI Engineer")

    if result:
        print("Matched Skills:", result["matched_skills"])
        print("Missing Skills:", result["missing_skills"])
        print("Skill Coverage:", round(result["coverage"], 2), "%")