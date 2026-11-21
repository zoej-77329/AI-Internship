# PathFinder — Final Professional Project Review & QA Audit

**Auditor:** Senior Software Engineer & QA Reviewer  
**Date:** 2026-11-21  
**Project:** PathFinder — Personalized Learning Path Recommendation System  
**Repository State:** Production Ready & Verified  

---

## 1. Executive Summary

PathFinder is a personalized learning path recommendation platform that connects user competencies to industry career benchmarks. The application analyzes user skill gaps, calculates content-based recommendations using TF-IDF vectorization and cosine similarity, generates prerequisite-ordered learning sequences via depth-first graph traversal, and tracks milestone progress using persistent SQLite storage.

The codebase has undergone a complete architectural, functional, security, and UI evaluation. All 35 automated tests pass with 100% success rate, the Streamlit server initializes cleanly with HTTP 200 OK, and all datasets and core algorithms are preserved.

---

## 2. Implemented Features

### 2.1 Core Engineering & Recommender Pipeline
- **Canonical Skill Normalization (`src/utils.py`)**: Maps 51 technology aliases to canonical names (preserving exact casing for `NumPy`, `OpenCV`, `GitHub`, `API`, `JavaScript`, etc.).
- **Skill Gap Diagnostics (`src/skill_analyzer.py`)**: Computes exact set operations for matched skills, missing skills, uncovered competencies, and percentage coverage against 10 industry roles.
- **Content-Based Similarity Engine (`src/similarity_engine.py`)**: Generates TF-IDF representations ($n$-gram range: 1–2) over course descriptions, titles, and competencies, matching missing skills via cosine similarity.
- **Dual-Metric Composite Ranking (`src/course_recommender.py`)**: Combines semantic alignment with direct skill coverage:
  $$\text{Ranking Score} = 0.70 \times \text{Similarity Score} + 0.30 \times \text{Skill Coverage Score}$$
- **Topological Learning Path Generator (`src/learning_path_generator.py`)**: Implements recursive DFS graph traversal with a `visiting_courses` recursion stack to resolve prerequisite dependencies and detect cycles.

### 2.2 Persistent Database Layer (`src/database.py`)
- **Engine**: SQLite3 (`data/pathfinder.db`), strictly excluded from Git.
- **Safety**: 100% parameterized SQL query execution (`?` parameter binding); zero dynamic string concatenation.
- **Connection Management**: Implemented `managed_connection` context manager to ensure all database connections are deterministically committed and closed upon exit, preventing resource and file handle leaks on Windows.
- **User Profile Management**: Persistent storage and retrieval of full name, career goal, normalized skills, experience level, and timestamps.
- **Progress Tracking**: Milestone status (`completion_status`, `completion_date`, `last_updated_date`) per course with real-time recalculation of hours and completion percentages.

### 2.3 EdTech SaaS UI Design System (`components/`)
- **Centralized Design System (`components/styles.py`)**: Consolidated typography (`Plus Jakarta Sans`), cohesive color palette (Primary Purple `#6957E8`, Deep Navy `#202747`, Light Canvas `#F5F6FC`), custom CSS, and Plotly theme helpers.
- **Executive Dashboard (`components/dashboard.py`)**: Real-time metrics, Plotly donut chart (readiness), horizontal competency gap chart, top-3 recommendation preview cards, and verified zero empty cards.
- **User Profile Settings (`components/profile_form.py`)**: Active profile card with validation, editing, and instant session cache invalidation.
- **Course Explorer Catalog (`components/course_explorer.py`)**: Multi-criteria search, difficulty level, category, and skill filters with sorting options.
- **Personalized Recommendations (`components/recommendation_view.py`)**: Ranked cards with mathematical formulas, difficulty badges, and comparative Plotly bar charts.
- **Topological Roadmap (`components/learning_path_view.py`)**: Step-by-step roadmap with live checkbox toggles synced to SQLite via `on_change` callbacks.
- **System Architecture View (`components/about_view.py`)**: Detailed methodology, formulas, system architecture, and tech stack overview.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Programming Language** | Python 3.11 |
| **Web Framework & UI** | Streamlit 1.35+, Custom Modern SaaS CSS |
| **Data Processing & ML** | Scikit-learn (TF-IDF Vectorizer, Cosine Similarity), Pandas 2.x, NumPy 2.x |
| **Visual Analytics** | Plotly Express & Plotly Graph Objects |
| **Data Storage & Persistence** | SQLite3 (ACID-compliant relational database) |
| **Testing & Quality Assurance** | Pytest 9.x, compileall |

---

## 4. Code Quality & Architecture Review

1. **Compilation & Syntax:**
   - Executed `python -m compileall src components app.py`: **0 errors**.
2. **Unused Imports & Dead Code Elimination:**
   - Identified and removed unused imports across `src/course_recommender.py`, `src/data_preprocessing.py`, `components/course_explorer.py`, `components/dashboard.py`, `components/learning_path_view.py`, `components/profile_form.py`, and `components/recommendation_view.py`.
3. **Database Resource Handling:**
   - Replaced raw `with get_connection:` blocks with a robust `@contextmanager managed_connection` that guarantees `conn.close()` execution in a `finally` block, resolving Windows SQLite file lock issues.
4. **Configuration & Directory Structure:**
   - Verified that `.streamlit/config.toml` is correctly located at the application root and removed redundant nested `.streamlit/.streamlit/` directory.
5. **Hardcoded Paths & Portability:**
   - Executed recursive pattern scans for local paths (`C:\`, `D:\`, user paths): **0 hardcoded paths found**. All paths dynamically derive from `Path(__file__).resolve().parent.parent`.

---

## 5. Security & Data Handling Review

1. **SQL Injection Vulnerabilities:**
   - Audited all SQL statements across `src/database.py`. All read, write, and upsert operations strictly use parameterized queries (`?`). No SQL statement concatenates raw strings.
2. **Secrets & Credentials:**
   - Audited repository for sensitive tokens, passwords, and API keys. **Zero credentials found**. The application does not require external API secrets.
3. **Git Cleanliness:**
   - `.gitignore` properly excludes `data/pathfinder.db`, `data/*.db`, `*.db-journal`, `*.db-wal`, `*.db-shm`, `__pycache__/`, `.pytest_cache/`, and `.venv/`.

---

## 6. Functional Consistency Verification

| Scenario | Expected Behavior | Observed Result | Status |
|---|---|---|---|
| **Profile Creation** | User inputs name, role, skills, level → persists in SQLite | Profile saved to SQLite table `user_profiles`, assigned `user_id = 1` | ✅ Passed |
| **Profile Update** | Modifying profile changes skills & experience | Record updated, `updated_at` timestamp refreshed | ✅ Passed |
| **Cache Invalidation** | Profile update triggers fresh recommendation calculation | Stale `recommendation_key` invalidated; new courses generated | ✅ Passed |
| **Prerequisite Precedence** | Beginner courses precede dependent intermediate courses | Python Fundamentals (Course 1) strictly precedes Machine Learning Fundamentals (Course 5) | ✅ Passed |
| **Progress Persistence** | Checkbox toggle in Learning Path saves milestone | Saved to `learning_progress` in SQLite; survives app reloads | ✅ Passed |
| **Course Catalog Search** | Searching "Python" returns only matching courses | Filtered 11 matching courses out of 30 | ✅ Passed |
| **Empty Input Handling** | Submitting empty name in profile form | Form validation displays error; invalid record rejected | ✅ Passed |

---

## 7. Automated Test Results

Executed with `python -m pytest -v`:

```
tests/test_course_recommender.py::test_recommendation_result_structure PASSED [  2%]
tests/test_course_recommender.py::test_recommendation_limit PASSED       [  5%]
tests/test_course_recommender.py::test_recommendation_columns PASSED     [  8%]
tests/test_data_loader.py::test_load_courses PASSED                      [ 11%]
tests/test_data_loader.py::test_load_career_skills PASSED                [ 14%]
tests/test_data_loader.py::test_load_processed_courses PASSED            [ 17%]
tests/test_data_loader.py::test_load_processed_career_skills PASSED      [ 20%]
tests/test_data_preprocessing.py::test_clean_courses PASSED              [ 22%]
tests/test_data_preprocessing.py::test_clean_careers PASSED              [ 25%]
tests/test_data_preprocessing.py::test_normalize_skill_column PASSED     [ 28%]
tests/test_database.py::test_database_initialization PASSED              [ 31%]
tests/test_database.py::test_profile_creation_and_retrieval PASSED       [ 34%]
tests/test_database.py::test_profile_update PASSED                       [ 37%]
tests/test_database.py::test_save_profile_helper PASSED                  [ 40%]
tests/test_database.py::test_profile_validation PASSED                   [ 42%]
tests/test_database.py::test_course_completion_and_progress_retrieval PASSED [ 45%]
tests/test_database.py::test_calculate_progress PASSED                   [ 48%]
tests/test_database.py::test_persistence_after_reopening_connection PASSED [ 51%]
tests/test_learning_path.py::test_learning_path_structure PASSED         [ 54%]
tests/test_learning_path.py::test_learning_path_step_order PASSED        [ 57%]
tests/test_learning_path.py::test_learning_path_duration PASSED          [ 60%]
tests/test_similarity_engine.py::test_recommendations_are_returned PASSED [ 62%]
tests/test_similarity_engine.py::test_unrelated_course_is_not_recommended PASSED [ 65%]
tests/test_similarity_engine.py::test_skill_coverage PASSED              [ 68%]
tests/test_similarity_engine.py::test_empty_missing_skills PASSED        [ 71%]
tests/test_similarity_engine.py::test_top_n_limit PASSED                 [ 74%]
tests/test_skill_analyzer.py::test_skill_coverage PASSED                 [ 77%]
tests/test_skill_analyzer.py::test_skill_normalization PASSED            [ 80%]
tests/test_skill_analyzer.py::test_invalid_career PASSED                 [ 82%]
tests/test_skill_analyzer.py::test_uncovered_skills PASSED               [ 85%]
tests/test_skill_analyzer.py::test_complete_report PASSED                [ 88%]
tests/test_utils.py::test_normalize_skill_canonical_cases PASSED         [ 91%]
tests/test_utils.py::test_normalize_skill_aliases PASSED                 [ 94%]
tests/test_utils.py::test_normalize_skill_edge_cases PASSED              [ 97%]
tests/test_utils.py::test_normalize_skill_list PASSED                    [100%]

============================= 35 passed in 6.04s ==============================
```

---

## 8. Known Limitations

1. **Catalog Domain Scope**: The current dataset contains 30 foundational courses across 10 career paths. Expanding the catalog would enable more granular specialization tracks.
2. **Single-User Local Storage**: The local SQLite architecture is optimized for single-user desktop exploration. A multi-tenant enterprise deployment would require user authentication and client-server database infrastructure (e.g. PostgreSQL).
3. **Static Duration Modeling**: Course duration values represent static estimated hours rather than dynamic, learner-paced completion models.

---

## 9. Installation and Execution Instructions

### Installation
```bash
# Clone repository and navigate to folder
cd PathFinder

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt
```

### Execution
```bash
# Launch Streamlit web application
streamlit run app.py
```

### Automated Testing
```bash
# Run complete test suite
python -m pytest -v
```

---

## 10. Final GitHub Readiness Status

- **Status:** **APPROVED FOR GITHUB REPOSITORY**
- No personal credentials or sensitive tokens exist in the repository.
- No temporary test scripts, virtual environments, or compiled `.pyc` caches are tracked.
- All documentation ([`README.md`](file:///d:/AI-Internship/Week-5/Learning-Path-Recommendation-System/README.md), [`docs/project_overview.md`](file:///d:/AI-Internship/Week-5/Learning-Path-Recommendation-System/docs/project_overview.md), [`docs/PROJECT_AUDIT.md`](file:///d:/AI-Internship/Week-5/Learning-Path-Recommendation-System/docs/PROJECT_AUDIT.md), [`docs/IMPLEMENTATION_PLAN.md`](file:///d:/AI-Internship/Week-5/Learning-Path-Recommendation-System/docs/IMPLEMENTATION_PLAN.md)) is complete and up-to-date.
