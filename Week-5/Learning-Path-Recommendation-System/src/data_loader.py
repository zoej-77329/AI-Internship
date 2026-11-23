import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"


def load_courses():
    return pd.read_csv(RAW_DATA_DIR / "courses.csv")


def load_career_skills():
    return pd.read_csv(RAW_DATA_DIR / "career_skills.csv")


def load_processed_courses():
    return pd.read_csv(PROCESSED_DATA_DIR / "courses_cleaned.csv")


def load_processed_career_skills():
    return pd.read_csv(PROCESSED_DATA_DIR / "career_skills_cleaned.csv")