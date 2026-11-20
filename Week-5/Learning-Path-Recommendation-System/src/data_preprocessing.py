
import pandas as pd

from src.data_loader import load_courses, load_career_skills


def explore_datasets():

    courses = load_courses()
    careers = load_career_skills()

    print("\n========== COURSE DATASET ==========")

    print("\nFirst 5 Rows:")
    print(courses.head())

    print("\nDataset Shape:")
    print(courses.shape)

    print("\nColumn Names:")
    print(courses.columns.tolist())

    print("\nData Types:")
    print(courses.dtypes)

    print("\nMissing Values:")
    print(courses.isnull().sum())

    print("\nDuplicate Rows:")
    print(courses.duplicated().sum())

    print("\nCourse Levels:")
    print(courses["level"].value_counts())

    print("\nCourse Categories:")
    print(courses["category"].value_counts())

    print("\n========== CAREER DATASET ==========")

    print("\nDataset Shape:")
    print(careers.shape)

    print("\nMissing Values:")
    print(careers.isnull().sum())

    print("\nDuplicate Rows:")
    print(careers.duplicated().sum())


if __name__ == "__main__":
    explore_datasets()


def clean_courses(courses):

    courses = courses.copy()

    # Remove duplicate course IDs
    courses = courses.drop_duplicates(subset=["course_id"])

    # Remove records without essential information
    courses = courses.dropna(
        subset=[
            "course_id",
            "course_name",
            "description",
            "skills",
            "level",
            "category",
            "duration_hours"
        ]
    )

    # Clean text columns
    text_columns = [
        "course_name",
        "description",
        "level",
        "category",
        "skills",
        "prerequisites"
    ]

    for column in text_columns:
        courses[column] = (
            courses[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # Standardize selected categorical values
    courses["level"] = courses["level"].str.title()
    courses["category"] = courses["category"].str.title()

    # Validate course duration
    courses["duration_hours"] = pd.to_numeric(
        courses["duration_hours"],
        errors="coerce"
    )

    courses = courses.dropna(subset=["duration_hours"])

    courses = courses[
        courses["duration_hours"] > 0
    ]

    # Validate allowed levels
    valid_levels = ["Beginner", "Intermediate", "Advanced"]

    courses = courses[
        courses["level"].isin(valid_levels)
    ]

    # Normalize skill separators and whitespace
    courses["skills"] = courses["skills"].apply(
        lambda value: "|".join(
            skill.strip()
            for skill in value.split("|")
            if skill.strip()
        )
    )

    courses["prerequisites"] = courses["prerequisites"].apply(
        lambda value: "|".join(
            skill.strip()
            for skill in value.split("|")
            if skill.strip()
        )
    )

    courses = courses.reset_index(drop=True)

    return courses


def clean_careers(careers):

    careers = careers.copy()

    careers = careers.drop_duplicates(
        subset=["career_goal"]
    )

    careers = careers.dropna(
        subset=["career_goal", "required_skills"]
    )

    careers["career_goal"] = (
        careers["career_goal"]
        .astype(str)
        .str.strip()
    )

    careers["description"] = (
        careers["description"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    careers["required_skills"] = (
        careers["required_skills"]
        .astype(str)
        .str.strip()
    )

    careers = careers[
        (careers["career_goal"] != "") &
        (careers["required_skills"] != "")
    ]

    careers = careers.reset_index(drop=True)

    return careers


SKILL_ALIASES = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ci/cd": "CI CD",
    "cicd": "CI CD",
    "tcp/ip": "TCP IP",
    "object oriented programming": "OOP"
}


def normalize_skill(skill):

    skill = skill.strip()

    normalized = SKILL_ALIASES.get(
        skill.lower(),
        skill
    )

    return normalized


def normalize_skill_column(data, column):

    data = data.copy()

    def normalize_list(value):

        skills = [
            normalize_skill(skill)
            for skill in str(value).split("|")
            if skill.strip()
        ]

        # Remove duplicate skills while preserving order
        return "|".join(dict.fromkeys(skills))

    data[column] = data[column].apply(normalize_list)

    return data


from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


def prepare_datasets():

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    courses = load_courses()
    careers = load_career_skills()

    cleaned_courses = clean_courses(courses)
    cleaned_careers = clean_careers(careers)

    cleaned_courses = normalize_skill_column(
        cleaned_courses,
        "skills"
    )

    cleaned_courses = normalize_skill_column(
        cleaned_courses,
        "prerequisites"
    )

    cleaned_careers = normalize_skill_column(
        cleaned_careers,
        "required_skills"
    )

    cleaned_courses.to_csv(
        PROCESSED_DATA_DIR / "courses_cleaned.csv",
        index=False
    )

    cleaned_careers.to_csv(
        PROCESSED_DATA_DIR / "career_skills_cleaned.csv",
        index=False
    )

    print("\nDatasets cleaned successfully!")

    print("Total courses:", len(cleaned_courses))
    print("Total career paths:", len(cleaned_careers))

    print("\nSaved files:")
    print("courses_cleaned.csv")
    print("career_skills_cleaned.csv")


if __name__ == "__main__":
    prepare_datasets()
    
def validate_datasets():

    courses_path = PROCESSED_DATA_DIR / "courses_cleaned.csv"
    careers_path = PROCESSED_DATA_DIR / "career_skills_cleaned.csv"

    courses = pd.read_csv(courses_path)
    careers = pd.read_csv(careers_path)

    print("\n========== VALIDATION REPORT ==========")

    print("\nCourses:")
    print("Rows:", len(courses))
    print("Missing values:")
    print(courses.isnull().sum())

    print("\nCareers:")
    print("Rows:", len(careers))
    print("Missing values:")
    print(careers.isnull().sum())

    print("\nCourse IDs unique:",
          courses["course_id"].is_unique)

    print("Career goals unique:",
          careers["career_goal"].is_unique)

    print("Invalid durations:",
          (courses["duration_hours"] <= 0).sum())


if __name__ == "__main__":
    prepare_datasets()
    validate_datasets()
