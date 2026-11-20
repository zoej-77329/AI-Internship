CANONICAL_SKILLS = {
    "python": "Python",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "api": "API",
    "rest api": "API",
    "opencv": "OpenCV",
    "github": "GitHub",
    "git": "Git",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "sql": "SQL",
    "oop": "OOP",
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "ci/cd": "CI CD",
    "cicd": "CI CD",
    "tcp/ip": "TCP IP",
    "tcp ip": "TCP IP",
    "object oriented programming": "OOP",
    "object-oriented programming": "OOP",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
    "data visualization": "Data Visualization",
    "data cleaning": "Data Cleaning",
    "project management": "Project Management",
    "quality assurance": "Quality Assurance",
    "neural networks": "Neural Networks",
    "model evaluation": "Model Evaluation",
    "cybersecurity": "Cybersecurity",
    "firebase": "Firebase",
    "flutter": "Flutter",
    "dart": "Dart",
    "flask": "Flask",
    "react": "React",
    "docker": "Docker",
    "devops": "DevOps",
    "aws": "AWS",
    "http": "HTTP",
    "nlp": "NLP",
    "agile": "Agile",
    "statistics": "Statistics",
    "probability": "Probability"
}


def normalize_skill(skill):
    skill = str(skill).strip()

    if not skill:
        return ""

    return CANONICAL_SKILLS.get(skill.casefold(), skill)


def normalize_skill_list(skills):
    normalized_skills = []
    seen = set()

    for skill in skills:
        normalized = normalize_skill(skill)

        if normalized and normalized.casefold() not in seen:
            normalized_skills.append(normalized)
            seen.add(normalized.casefold())

    return normalized_skills