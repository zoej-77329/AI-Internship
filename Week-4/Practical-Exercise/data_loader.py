import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

def load_courses():
    file_path = DATASET_DIR / "courses.csv"
    courses = pd.read_csv(file_path)

    courses["skills"] = courses["skills"].fillna("")

    courses["skills"] = courses["skills"].apply(
        lambda x: [skill.strip() for skill in x.split("|") if skill.strip()]
    )

    return courses


def load_career_skills():
    file_path = DATASET_DIR / "career_skills.csv"
    careers = pd.read_csv(file_path)

    careers["required_skills"] = careers["required_skills"].apply(
        lambda x: [skill.strip() for skill in x.split("|") if skill.strip()]
    )

    return careers


if __name__ == "__main__":
    courses = load_courses()
    careers = load_career_skills()

    print("Courses Dataset:")
    print(courses.head())

    print("\nCareer Skills Dataset:")
    print(careers.head())