# PathFinder — Personalized Learning Path Recommendation System

> **"Personalized learning. Clear career direction."**

PathFinder is an EdTech SaaS platform designed to bridge technical skill gaps. By evaluating a learner's existing competencies against industry benchmarks, PathFinder provides algorithmic course recommendations and generates an ordered, prerequisite-aware learning roadmap backed by persistent local storage.

---

## 🌟 Key Features

1. **Executive Dashboard**:
   - Real-time skill readiness metric and match percentage.
   - Interactive Plotly donut and comparative competency gap charts.
   - Top course recommendations preview with difficulty badges and duration.
   - Live learning path completion tracker calculated directly from SQLite.

2. **My Profile (Persistent Settings)**:
   - Configure learner name, experience level, target career role, and existing skills.
   - Persistent storage in SQLite (`data/pathfinder.db`) ensuring user profiles survive application restarts.
   - Auto-recalibration of recommendations whenever career goals or skills are updated.

3. **Course Explorer (Curated Catalog)**:
   - Full-text search across titles, descriptions, and competencies.
   - Multi-criteria filtering by difficulty level, domain category, and specific skills.
   - Multi-option sorting (by duration, name, course ID).
   - Detailed cards highlighting acquired skills, prerequisites, and duration.

4. **Algorithmic Course Recommendations**:
   - Content-based TF-IDF vectorization ($n$-gram range: 1–2) and Cosine Similarity against missing skill queries.
   - Dual-metric composite ranking:
     $$\text{Ranking Score} = 0.70 \times \text{Similarity Score} + 0.30 \times \text{Skill Coverage Score}$$
   - Comparative Plotly bar chart comparing relevance and coverage.
   - Clear distinction between mathematical relevance indicators and academic success forecasts.

5. **Topological Learning Roadmap**:
   - Depth-First Search (DFS) topological sort with cycle detection to ensure all prerequisites are mastered first.
   - Sequential step numbering with duration, level, and competency badges.
   - Interactive completion checkboxes synchronized immediately to SQLite.
   - Milestone completion celebrations and remaining hours tracking.

6. **System Architecture & Methodology (About View)**:
   - Complete technical breakdown of the recommendation algorithm, graph traversal, and project scope.

---

## 🏗️ Technology Stack

- **Language & Runtime**: Python 3.11
- **UI Framework**: Streamlit (SaaS design system, custom CSS, native components)
- **Data Science & ML**: Scikit-Learn (TF-IDF Vectorizer, Cosine Similarity), Pandas, NumPy
- **Visual Analytics**: Plotly Express & Plotly Graph Objects
- **Database & Persistence**: SQLite3 with parameterized SQL queries
- **Testing**: Pytest (35 automated tests)

---

## 📁 Project Structure

```
Learning-Path-Recommendation-System/
├── .streamlit/
│   └── config.toml                  # Streamlit server & theme configuration
├── components/
│   ├── __init__.py
│   ├── styles.py                    # Centralized SaaS design system & CSS
│   ├── dashboard.py                 # Executive overview & charts
│   ├── profile_form.py              # Profile management & validation
│   ├── course_explorer.py           # Catalog search & filtering
│   ├── recommendation_view.py       # Ranked recommendation analytics
│   ├── learning_path_view.py        # Topological roadmap & completion tracking
│   └── about_view.py                # System methodology & architecture
├── data/
│   ├── raw/
│   │   ├── courses.csv              # Raw course dataset
│   │   └── career_skills.csv        # Raw career goals & required skills
│   ├── processed/
│   │   ├── courses_cleaned.csv      # Cleaned course dataset
│   │   └── career_skills_cleaned.csv# Cleaned career requirements
│   └── pathfinder.db                # SQLite database (excluded from Git)
├── docs/
│   ├── PROJECT_AUDIT.md             # Comprehensive technical audit report
│   ├── IMPLEMENTATION_PLAN.md       # Phased roadmap & execution plan
│   └── project_overview.md          # Architectural documentation
├── src/
│   ├── __init__.py
│   ├── database.py                  # Modular SQLite storage layer
│   ├── data_loader.py               # Dataset loading functions
│   ├── data_preprocessing.py        # Data cleaning & validation pipeline
│   ├── skill_analyzer.py            # Skill gap analysis engine
│   ├── similarity_engine.py         # TF-IDF & Cosine Similarity recommender
│   ├── course_recommender.py        # Recommendation orchestrator
│   ├── learning_path_generator.py   # Topological sort with cycle detection
│   └── utils.py                     # Canonical skill normalization (51 terms)
├── tests/
│   ├── test_data_loader.py          # Data loading tests
│   ├── test_data_preprocessing.py   # Data cleaning & normalization tests
│   ├── test_database.py             # SQLite persistence & progress tests
│   ├── test_skill_analyzer.py       # Skill gap analysis tests
│   ├── test_similarity_engine.py    # Recommendation algorithm tests
│   ├── test_course_recommender.py   # Integration tests
│   ├── test_learning_path.py        # Topological roadmap tests
│   ├── test_utils.py                # Canonical skill normalizer tests
│   └── skill_visualization.py       # Matplotlib visualization utility
├── app.py                           # Main application entry point
├── requirements.txt                 # Pinned project dependencies
└── README.md                        # Project documentation
```

---

## 🚀 Installation & Running

### 1. Prerequisites
- Python 3.11+
- Virtual environment (recommended)

### 2. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```

### 4. Run the Automated Test Suite
```bash
python -m pytest -v
```

All 35 unit and integration tests validate database persistence, topological sorting, similarity calculations, and preprocessing.
