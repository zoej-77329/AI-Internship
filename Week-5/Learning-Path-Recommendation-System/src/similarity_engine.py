import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data_loader import load_processed_courses
from src.utils import normalize_skill_list


def get_course_skills(skill_text):
    if pd.isna(skill_text):
        return []

    return normalize_skill_list(str(skill_text).split("|"))


def build_course_text(course):
    name = str(course.get("course_name", ""))
    description = str(course.get("description", ""))

    skills = get_course_skills(course.get("skills", ""))

    return f"{name} {description} {' '.join(skills)}"


def recommend_courses(missing_skills, top_n=5, courses=None):

    missing_skills = normalize_skill_list(missing_skills)

    columns = [
        "course_id",
        "course_name",
        "skills",
        "level",
        "duration_hours",
        "matched_skills",
        "skill_coverage",
        "similarity_score",
        "ranking_score"
    ]

    if not missing_skills:
        return pd.DataFrame(columns=columns)

    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if courses is None:
        courses = load_processed_courses()

    if courses.empty:
        return pd.DataFrame(columns=columns)

    course_texts = courses.apply(build_course_text, axis=1).tolist()

    user_query = " ".join(missing_skills)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b\w+\b"
    )

    try:
        course_vectors = vectorizer.fit_transform(course_texts)
        user_vector = vectorizer.transform([user_query])

    except ValueError:
        return pd.DataFrame(columns=columns)

    similarity_scores = cosine_similarity(
        user_vector,
        course_vectors
    ).flatten()

    results = []

    for index, (_, course) in enumerate(courses.iterrows()):

        course_skills = get_course_skills(course["skills"])

        matched_skills = [
            skill for skill in missing_skills
            if skill.casefold() in {
                item.casefold() for item in course_skills
            }
        ]

        coverage = (
            len(matched_skills) / len(missing_skills)
        ) * 100

        similarity_score = float(similarity_scores[index]) * 100

        ranking_score = (
            0.70 * similarity_score
            + 0.30 * coverage
        )

        if similarity_score > 0 or coverage > 0:

            results.append({
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "skills": course["skills"],
                "level": course["level"],
                "duration_hours": course["duration_hours"],
                "matched_skills": matched_skills,
                "skill_coverage": round(coverage, 2),
                "similarity_score": round(similarity_score, 2),
                "ranking_score": round(ranking_score, 2)
            })

    if not results:
        return pd.DataFrame(columns=columns)

    recommendations = pd.DataFrame(results)

    recommendations = recommendations.sort_values(
        by=["ranking_score", "skill_coverage"],
        ascending=False
    )

    return recommendations.head(top_n).reset_index(drop=True)


if __name__ == "__main__":

    missing_skills = [
        "Machine Learning",
        "Python",
        "Statistics"
    ]

    recommendations = recommend_courses(
        missing_skills,
        top_n=5
    )

    print("\nRecommended Courses")
    print("-------------------")

    if recommendations.empty:
        print("No matching courses found.")

    else:
        print(
            recommendations[
                [
                    "course_name",
                    "matched_skills",
                    "skill_coverage",
                    "similarity_score",
                    "ranking_score"
                ]
            ].to_string(index=False)
        )