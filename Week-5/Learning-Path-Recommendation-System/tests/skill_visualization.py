import matplotlib.pyplot as plt

from src.skill_analyzer import generate_skill_gap_report


user_skills = ["Python", "Pandas", "NumPy"]

report = generate_skill_gap_report(
    user_skills,
    "AI Engineer"
)

matched = len(report["matched_skills"])
missing = len(report["missing_skills"])

labels = ["Matched Skills", "Missing Skills"]
values = [matched, missing]

plt.figure(figsize=(7, 5))

plt.bar(labels, values)

plt.title("Career Skill Gap Analysis")
plt.ylabel("Number of Skills")

plt.tight_layout()
plt.show()