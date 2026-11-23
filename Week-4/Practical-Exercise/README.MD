# – Mini Learning Path Recommendation System

## Objective
Develop a small recommendation system by combining the concepts learned during the first four days of Week 4.

## Features
- Load course and career-skill datasets.
- Analyze the user's current skills.
- Identify missing skills for a selected career.
- Calculate course similarity using TF-IDF and cosine similarity.
- Rank courses based on similarity and skill coverage.
- Generate a learning path using prerequisite checks.

## Technologies
- Python
- Pandas
- Scikit-learn
- TF-IDF
- Cosine Similarity

## Project Structure
- `data_loader.py` – Loads and prepares datasets.
- `skill_gap.py` – Identifies missing skills.
- `course_recommender.py` – Calculates course recommendations.
- `learning_path.py` – Generates a prerequisite-aware learning sequence.
- `main.py` – Runs the complete system.

## How to Run

Install dependencies:

```bash
python -m pip install pandas numpy scikit-learn
```

Run the application:

```bash
python main.py
```

## Learning Outcome
Practiced data preparation, skill-gap analysis, similarity matching, course ranking, and basic learning-path generation.
