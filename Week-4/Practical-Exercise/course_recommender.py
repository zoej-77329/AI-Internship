from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data_loader import load_courses


def recommend_courses(missing_skills):

    courses = load_courses()

    if not missing_skills:
        print("No missing skills. No recommendations needed.")
        return courses.iloc[0:0].copy()

    # Convert course skills into text
    course_text = courses["skills"].apply(
        lambda skills: " ".join(skills)
    ).tolist()

    # Convert missing skills into text
    user_text = " ".join(sorted(missing_skills))

    # Create TF-IDF vectors using one shared vocabulary
    vectorizer = TfidfVectorizer()

    course_vectors = vectorizer.fit_transform(course_text)
    user_vector = vectorizer.transform([user_text])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        user_vector,
        course_vectors
    )[0]

    # Calculate missing skill coverage
    coverage_scores = []

    for skills in courses["skills"]:

        covered = set(skills).intersection(missing_skills)

        coverage = (
            len(covered) / len(missing_skills) * 100
        )

        coverage_scores.append(coverage)

    # Combine scores
    courses["similarity"] = similarity_scores * 100
    courses["coverage"] = coverage_scores

    courses["recommendation_score"] = (
        courses["similarity"] * 0.4 +
        courses["coverage"] * 0.6
    )

    # Keep only relevant courses
    recommendations = courses[
        courses["coverage"] > 0
    ].copy()

    recommendations = recommendations.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return recommendations


if __name__ == "__main__":

    missing_skills = {
        "Statistics",
        "Machine Learning",
        "Deep Learning"
    }

    results = recommend_courses(missing_skills)

    print(
        results[
            [
                "course_name",
                "skills",
                "similarity",
                "coverage",
                "recommendation_score"
            ]
        ].to_string(index=False)
    )