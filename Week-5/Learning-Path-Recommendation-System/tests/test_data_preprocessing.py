import pandas as pd
from src.data_preprocessing import clean_courses, clean_careers, normalize_skill_column


def test_clean_courses():
    raw_data = pd.DataFrame([
        {
            "course_id": 1,
            "course_name": "Course A",
            "description": "Desc A",
            "skills": "Python|SQL",
            "level": "beginner",
            "category": "programming",
            "duration_hours": 10,
            "prerequisites": ""
        },
        {
            "course_id": 1,  # Duplicate ID
            "course_name": "Course A Dup",
            "description": "Desc A",
            "skills": "Python",
            "level": "beginner",
            "category": "programming",
            "duration_hours": 10,
            "prerequisites": ""
        },
        {
            "course_id": 2,
            "course_name": "Course B",
            "description": "Desc B",
            "skills": "Python",
            "level": "expert",  # Invalid level
            "category": "programming",
            "duration_hours": 10,
            "prerequisites": ""
        },
        {
            "course_id": 3,
            "course_name": "Course C",
            "description": "Desc C",
            "skills": "Python",
            "level": "Intermediate",
            "category": "data science",
            "duration_hours": -5,  # Invalid duration
            "prerequisites": "Python"
        }
    ])

    cleaned = clean_courses(raw_data)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["course_id"] == 1
    assert cleaned.iloc[0]["level"] == "Beginner"
    assert cleaned.iloc[0]["category"] == "Programming"


def test_clean_careers():
    raw_data = pd.DataFrame([
        {
            "career_goal": "Data Scientist",
            "description": "Analyzes data",
            "required_skills": "Python|Pandas|SQL"
        },
        {
            "career_goal": "Data Scientist",  # Duplicate
            "description": "Duplicate entry",
            "required_skills": "Python"
        },
        {
            "career_goal": "",  # Empty
            "description": "No title",
            "required_skills": "Python"
        }
    ])

    cleaned = clean_careers(raw_data)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["career_goal"] == "Data Scientist"


def test_normalize_skill_column():
    data = pd.DataFrame({
        "skills": ["python|ml|NumPy|python", "js|ci/cd"]
    })
    normalized = normalize_skill_column(data, "skills")
    assert normalized.iloc[0]["skills"] == "Python|Machine Learning|NumPy"
    assert normalized.iloc[1]["skills"] == "JavaScript|CI CD"
