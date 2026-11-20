
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"


def load_courses():

    file_path = RAW_DATA_DIR / "courses.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Course dataset not found: {file_path}")

    return pd.read_csv(file_path)


def load_career_skills():

    file_path = RAW_DATA_DIR / "career_skills.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Career dataset not found: {file_path}")

    return pd.read_csv(file_path)


if __name__ == "__main__":

    courses = load_courses()
    careers = load_career_skills()

    print("Courses loaded:", len(courses))
    print("Career paths loaded:", len(careers))

    print("\nCourse Dataset:")
    print(courses.head())

    print("\nCareer Skills Dataset:")
    print(careers.head())
