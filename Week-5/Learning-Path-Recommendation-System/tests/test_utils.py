from src.utils import normalize_skill, normalize_skill_list


def test_normalize_skill_canonical_cases():
    # Technical names preserving exact case
    assert normalize_skill("numpy") == "NumPy"
    assert normalize_skill("NumPy") == "NumPy"
    assert normalize_skill("github") == "GitHub"
    assert normalize_skill("GitHub") == "GitHub"
    assert normalize_skill("opencv") == "OpenCV"
    assert normalize_skill("OpenCV") == "OpenCV"
    assert normalize_skill("api") == "API"
    assert normalize_skill("API") == "API"
    assert normalize_skill("javascript") == "JavaScript"
    assert normalize_skill("js") == "JavaScript"


def test_normalize_skill_aliases():
    assert normalize_skill("ml") == "Machine Learning"
    assert normalize_skill("machine learning") == "Machine Learning"
    assert normalize_skill("ai") == "Artificial Intelligence"
    assert normalize_skill("ci/cd") == "CI CD"
    assert normalize_skill("cicd") == "CI CD"
    assert normalize_skill("tcp/ip") == "TCP IP"
    assert normalize_skill("object oriented programming") == "OOP"
    assert normalize_skill("sklearn") == "Scikit-learn"


def test_normalize_skill_edge_cases():
    assert normalize_skill("") == ""
    assert normalize_skill("   ") == ""
    assert normalize_skill("UnknownSkillXYZ") == "UnknownSkillXYZ"


def test_normalize_skill_list():
    raw_skills = ["python", "ml", "NumPy", "numpy", "api", "API", "  "]
    result = normalize_skill_list(raw_skills)
    assert result == ["Python", "Machine Learning", "NumPy", "API"]
