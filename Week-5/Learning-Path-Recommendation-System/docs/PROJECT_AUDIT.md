# PathFinder — Project Technical Audit

> Audit performed: 2026-11-21  
> Auditor: Automated deep-scan of every Python, CSV, TOML and Markdown file in the project.

---

## 1. Project Inventory

| File / Path | Size | Status |
|---|---|---|
| `app.py` | 569 lines | ✅ Present |
| `components/__init__.py` | 0 bytes | ✅ Present (empty, correct) |
| `components/profile_form.py` | 132 lines | ✅ Present |
| `components/dashboard.py` | 226 lines | ✅ Present |
| `components/recommendation_view.py` | 152 lines | ✅ Present |
| `components/learning_path_view.py` | 272 lines | ✅ Present |
| `src/__init__.py` | 0 bytes | ✅ Present (empty, correct) |
| `src/data_loader.py` | 22 lines | ✅ Present |
| `src/data_preprocessing.py` | 313 lines | ⚠️ Structural issues |
| `src/skill_analyzer.py` | 91 lines | ✅ Present |
| `src/similarity_engine.py` | 156 lines | ✅ Present |
| `src/course_recommender.py` | 111 lines | ✅ Present |
| `src/learning_path_generator.py` | 213 lines | ✅ Present |
| `src/utils.py` | 78 lines | ✅ Present |
| `data/raw/courses.csv` | 30 rows, 8 cols | ✅ Present |
| `data/raw/career_skills.csv` | 10 rows, 3 cols | ✅ Present |
| `data/processed/courses_cleaned.csv` | 30 rows, 8 cols | ✅ Present |
| `data/processed/career_skills_cleaned.csv` | 10 rows, 3 cols | ✅ Present |
| `tests/test_data_loader.py` | 0 bytes | ❌ Empty |
| `tests/test_skill_analyzer.py` | 65 lines | ✅ Present |
| `tests/test_course_recommender.py` | 45 lines | ✅ Present |
| `tests/test_learning_path.py` | 52 lines | ✅ Present |
| `tests/test_similarity_engine.py` | 81 lines | ✅ Present |
| `tests/skill_visualization.py` | 27 lines | ⚠️ Misplaced |
| `.streamlit/.streamlit/config.toml` | 10 lines | ❌ Wrong nesting |
| `requirements.txt` | 7 entries | ⚠️ Incomplete |
| `README.md` | 53 lines | ⚠️ Outdated |
| `docs/project_overview.md` | 0 bytes | ❌ Empty |

---

## 2. Features That Work Correctly

### ✅ Data Layer
- `data_loader.py` — All four load functions (`load_courses`, `load_career_skills`, `load_processed_courses`, `load_processed_career_skills`) use `pathlib.Path` with correct relative anchoring from `__file__`. Paths resolve correctly regardless of working directory.
- Processed CSVs are present and have no missing values in essential columns.

### ✅ Skill Analysis
- `skill_analyzer.get_career_requirements()` — Performs case-insensitive career goal lookup, returns normalized skill list.
- `skill_analyzer.analyze_skills()` — Returns all required keys: `user_skills`, `required_skills`, `matched_skills`, `missing_skills`, `extra_skills`, `coverage`.
- `skill_analyzer.identify_uncovered_skills()` — Correctly identifies missing skills that have no matching course.
- `skill_analyzer.generate_skill_gap_report()` — Correctly assembles the full report including `uncovered_skills`, `covered_missing_skills`, and `career_goal`.

### ✅ Similarity Engine
- `similarity_engine.recommend_courses()` — TF-IDF + cosine similarity pipeline runs correctly. Returns all expected columns: `course_id`, `course_name`, `skills`, `level`, `duration_hours`, `matched_skills`, `skill_coverage`, `similarity_score`, `ranking_score`.
- Edge cases handled: empty skill list → empty DataFrame; empty course set → empty DataFrame; `ValueError` from vectorizer caught.
- Ranking score formula (`0.70 * similarity + 0.30 * coverage`) is consistent.

### ✅ Course Recommender
- `course_recommender.get_personalized_recommendations()` — All five steps (skill gap → filter → recommend → reason → return) work correctly.
- Returns all expected keys: `career_goal`, `skill_report`, `recommendations`, `total_recommendations`, `uncovered_skills`.
- `recommendation_reason` column is populated correctly.
- Optional `level` and `max_duration` filters work.

### ✅ Learning Path Generator
- `learning_path_generator.generate_learning_path()` — Prerequisite-aware topological sort (DFS with cycle detection) is implemented correctly.
- Returns all expected keys: `career_goal`, `learning_path`, `total_courses`, `total_duration`, `unresolved_prerequisites`, `skill_report`.
- DataFrame columns are correct: `step`, `course_id`, `course_name`, `level`, `duration_hours`, `skills`, `prerequisites`, `cumulative_duration`.
- `split_skills()` safely handles `NaN`, `None`, and empty strings from the prerequisites column.
- Circular dependency detection via `visiting_courses` set prevents infinite recursion.

### ✅ Skill Normalization — `src/utils.py`
- `utils.normalize_skill()` and `normalize_skill_list()` preserve technical names correctly: `NumPy`, `GitHub`, `OpenCV`, `API`, `JavaScript`, `CI CD`.
- The canonical dictionary (`CANONICAL_SKILLS`) covers 51 skill aliases and is used at runtime by all backend modules (`skill_analyzer`, `similarity_engine`, `learning_path_generator`).

### ✅ Profile Form
- `profile_form.display_profile_form()` — Loads career goals and available skills from processed CSVs. Pre-fills form from existing `session_state`. Saves profile dict with correct keys: `name`, `career_goal`, `current_skills`, `experience_level`. Clears stale recommendation keys on save.

### ✅ Dashboard
- `dashboard.display_dashboard()` — Consumes `result` dict correctly. All four metric cards populated from real data. Skill progress bar uses live `coverage` float. Matched/missing skill tags rendered via HTML. Top-3 course preview renders correctly.

### ✅ Recommendation View
- `recommendation_view.display_recommendations()` — Full course cards with live Plotly bar chart. Accesses all required columns from the recommendations DataFrame. Correctly reads `uncovered_skills` from the result dict.

### ✅ Learning Path View (Core Logic)
- `learning_path_view.display_learning_path()` — Calls `generate_learning_path()` correctly. Reads all DataFrame columns used in rendering (`step`, `course_id`, `course_name`, `level`, `duration_hours`, `skills`, `prerequisites`). Checkbox-based progress tracking via `get_progress_key()` uses a deterministic, collision-resistant key scheme.

### ✅ App Navigation
- `app.py` sidebar radio navigation routes correctly to all four pages.
- Recommendation engine is called once per unique `(career_goal, sorted_skills)` combination and cached in session state; it does not re-run on every Streamlit rerun.

---

## 3. Bugs and Integration Problems

### 🔴 BUG-01 — Streamlit config.toml in wrong location (Critical)
**File:** `.streamlit/.streamlit/config.toml`  
**Expected location:** `.streamlit/config.toml`

The config file is nested one directory too deep inside a spurious inner `.streamlit` subfolder. Streamlit will not read it; the application runs with default theme, colors and `runOnSave` will be ignored.

**Impact:** Theme customization (purple accent, background color, font) set in `config.toml` is silently ignored. The CSS injected in `app.py` partially compensates for this, but `runOnSave = true` does not work.

---

### 🔴 BUG-02 — "Create My Profile" buttons are dead (Critical)
**File:** `app.py` — Lines 466, 538, 567

All three "Create My Profile" / "Create Profile" CTA buttons set `st.session_state["open_profile"] = True` and call `st.rerun()`. However, **`open_profile` is never read anywhere in `app.py`**. The `page` variable is always determined by `st.radio`, which is not changed by this code. After rerun, the page stays on Dashboard/Recommendations/Learning Path. The user cannot navigate to the profile form by clicking these buttons.

**Impact:** New users who land on Dashboard and click "Create My Profile" are stuck. The app appears broken on first use.

---

### 🔴 BUG-03 — Learning path regenerated on every checkbox toggle (Performance / UX Critical)
**File:** `components/learning_path_view.py` — Line 41

`generate_learning_path()` is called unconditionally inside `display_learning_path()`. Every time a user checks or unchecks a "Mark as completed" checkbox, Streamlit reruns the script, which re-runs the full TF-IDF + prerequisite-resolution pipeline. This causes visible lag and potentially inconsistent path results between renders.

**Impact:** Noticeable UI freeze on every progress checkbox interaction. Progress counting at the top of the page is calculated **before** checkboxes are rendered; the displayed metrics are always one click behind (stale progress). The re-calculation at the bottom of the function (Lines 209–224) is correct, but the top metrics (Lines 108–126) show the **previous** state.

---

### 🔴 BUG-04 — Progress metrics shown before checkboxes render (Stale State)
**File:** `components/learning_path_view.py` — Lines 77–126 vs Lines 209–224

`completed_courses` and `progress_percentage` are computed **before** `st.checkbox()` widgets are rendered. In Streamlit, checkbox state from the current rerun is already in `session_state` when it is read, so the top metrics correctly reflect the state **after** the last checkbox click. However this is fragile: if any checkbox key is missing from session state on first load, the displayed progress will be 0/N even though the user has previously completed courses. Combined with BUG-03 (path regeneration), the first render after a checkbox click can show inconsistent numbers.

---

### 🟡 BUG-05 — `data_preprocessing.py` has duplicate `if __name__ == "__main__"` blocks and duplicate imports (Structural)
**File:** `src/data_preprocessing.py` — Lines 50, 278, 311

The file contains **three** `if __name__ == "__main__":` blocks:
- Line 50: calls `explore_datasets()` only.
- Line 278: calls `prepare_datasets()`.
- Line 311: calls `prepare_datasets()` **and** `validate_datasets()` — this is a duplicate.

Additionally, `from pathlib import Path` is imported twice (Lines 2 and 223), and `PROJECT_DIR` is defined twice (Lines 4 and 225). The second definitions are redundant dead code.

**Impact:** No runtime failure (Python only uses the last `__main__` block when run directly). The duplicate `prepare_datasets()` call would run twice if the second `__main__` block were ever reached, which would re-write the CSVs unnecessarily. The structure is confusing to read and maintain.

---

### 🟡 BUG-06 — Two separate normalizer dictionaries with different coverage (Consistency)
**Files:** `src/data_preprocessing.py` (SKILL_ALIASES, 9 entries) and `src/utils.py` (CANONICAL_SKILLS, 51 entries)

`data_preprocessing.py` defines its own `SKILL_ALIASES` with only 9 mappings. `src/utils.py` defines `CANONICAL_SKILLS` with 51 mappings. All runtime backend modules import from `src/utils.py`. The preprocessing pipeline (`prepare_datasets()`) uses the smaller `data_preprocessing.normalize_skill`. Because the raw CSVs already use correct casing (NumPy, GitHub, OpenCV, API, etc.), this does not corrupt the processed data in practice — but if the raw data ever contains lowercase aliases like `'numpy'`, `'github'`, `'api'`, `'opencv'` in the raw CSVs, `data_preprocessing.normalize_skill` would leave them unnormalized. The inconsistency is a latent bug and a maintainability risk.

---

### 🟡 BUG-07 — `recommendation_view.py` course numbering depends on DataFrame index (Minor)
**File:** `components/recommendation_view.py` — Line 84

```python
for index, course in recommendations.iterrows():
    st.markdown(f"### {index + 1}. {course['course_name']}")
```

`iterrows()` yields the DataFrame's internal index. The recommendations DataFrame is `reset_index(drop=True)` in `similarity_engine.py`, so this currently returns `0, 1, 2 …` and `index + 1` = `1, 2, 3 …`. This is correct **now**, but it is fragile: any future code that skips `reset_index()` or applies additional filtering before passing the DataFrame to this component would produce wrong numbering. The intent should be to use the loop's rank, not the internal index.

---

### 🟡 BUG-08 — Duplicate CSS rules in `app.py` (Cosmetic / Maintainability)
**File:** `app.py`

Three CSS selector sets are defined twice, with the later definition silently overriding the first:

| Selector | First defined | Second defined |
|---|---|---|
| `h1, h2, h3` | Line 53 | `h1, h2, h3, h4` at Line 293 |
| `.stButton button` | Lines 207–224 | Lines 248–270 |
| `[data-testid="stVerticalBlockBorderWrapper"]` | Lines 300–306 | Lines 317–319 |

**Impact:** The second block wins (CSS cascade). The first definition is dead. This makes the stylesheet harder to maintain and may confuse future theme changes.

---

### 🟡 BUG-09 — `tests/skill_visualization.py` is misplaced and not a test file
**File:** `tests/skill_visualization.py`

This script runs top-level code (calls `generate_skill_gap_report()` and `plt.show()`) when imported. It is **not** a pytest test (no `test_` prefix on functions), yet it lives in `tests/`. Pytest will collect and try to execute it, which will block on `plt.show()` or fail depending on the environment.

---

### 🟡 BUG-10 — `tests/test_data_loader.py` is completely empty
**File:** `tests/test_data_loader.py`

The file exists but contains zero lines. There are no tests for the data loader module (`load_courses`, `load_career_skills`, `load_processed_courses`, `load_processed_career_skills`).

---

### 🟡 BUG-11 — `pytest` and `streamlit` / `plotly` are not installed in the active environment
**Environment check**

The project's `pip list` confirms `streamlit`, `plotly`, and `pytest` are **not installed** in the Python 3.11.5 environment used by this machine. The `requirements.txt` lists them, but the environment has not been set up from it. Running `python -m pytest tests/` currently fails with `No module named pytest`.

---

### 🟡 BUG-12 — `open_profile` session state key is set but never consumed (Dead code)
**File:** `app.py` — Lines 466, 538, 567

See BUG-02. Additionally, the orphaned `open_profile` key will accumulate in session state without ever being cleared.

---

## 4. Dataset Quality

| Property | courses.csv | career_skills.csv |
|---|---|---|
| Rows | 30 | 10 |
| Columns | 8 | 3 |
| Duplicates | None | None |
| Missing essentials | None | None |
| Missing prerequisites | 13 rows (NaN) | N/A |
| Skill separator | `|` | `|` |
| Skill casing | Correct (Title Case / proper nouns) | Correct |

### Observations

1. **13 NaN prerequisites** — This is correct data: beginner-level courses genuinely have no prerequisites. `split_skills()` handles `NaN` safely. `clean_courses()` fills prerequisites with `""` before saving. However, the processed CSV shows these as `NaN` (not empty string), because `fillna("")` happens on a copy but the `dropna()` subset does not include `prerequisites`, meaning the fill does not apply to the saved file. This is cosmetically inconsistent but functionally safe because `split_skills()` checks `pd.isna()`.

2. **Small dataset (30 courses, 10 careers)** — The dataset is minimal. Some career goals (e.g. "Machine Learning Engineer") require skills like `Docker` that map to only 1 course. High-skill-gap users will get very short learning paths.

3. **Prerequisite chain depth** — The prerequisite graph is at most 2 levels deep (e.g., Python → Machine Learning → Deep Learning). The DFS cycle detector is correct and would handle deeper chains.

4. **"Database" skill** — `courses.csv` lists "Database" as a skill, but `career_skills.csv` does not require it for any career goal. It is an extra skill that will never surface as a recommendation target.

5. **"Programming" skill** — Similarly listed in courses but not required by any career. REST API Development (course 14) requires "Programming" as a prerequisite, but no career goal lists "Programming" as required.

6. **`Authentication` and `Containers`** — Appear in course skills but not in any career's required skills. These courses will only be recommended if their text similarity score is high enough.

---

## 5. UI Problems

| # | Location | Issue | Severity |
|---|---|---|---|
| UI-01 | `app.py` Lines 466, 538, 567 | "Create My Profile" buttons trigger `open_profile=True` + `rerun()` but no page change occurs | 🔴 Critical |
| UI-02 | `components/learning_path_view.py` Lines 108–126 | Progress metrics shown at top are stale by one rerun when checkboxes are toggled | 🟡 Medium |
| UI-03 | `app.py` Lines 300–324 | `[data-testid="stVerticalBlockBorderWrapper"]` defined twice; hover styles partly shadowed | 🟡 Low |
| UI-04 | `app.py` Lines 53 and 293 | `h1, h2, h3` defined twice; second block adds `h4` but shadows the first block | 🟡 Low |
| UI-05 | `app.py` Lines 207–270 | `.stButton button` defined twice — first block shadowed by second block | 🟡 Low |
| UI-06 | `components/dashboard.py` Lines 76 and 135 | `<div class="custom-card">` opened with `st.markdown()` but closed with another `st.markdown("</div>")` — these are raw HTML strings injected into Streamlit's DOM; Streamlit may strip or reorder them | 🟡 Medium |
| UI-07 | `.streamlit/` directory | `config.toml` is at `.streamlit/.streamlit/config.toml` instead of `.streamlit/config.toml` — theme and server settings are silently ignored | 🔴 Critical |

---

## 6. Testing Problems

| # | File | Problem |
|---|---|---|
| T-01 | `tests/test_data_loader.py` | File is completely empty. Zero coverage of `data_loader.py`. |
| T-02 | `tests/skill_visualization.py` | Not a test file. Runs matplotlib blocking code at module level. Must be excluded from pytest or moved. |
| T-03 | All test files | `pytest` is not installed in the active environment. No tests can run without `pip install pytest`. |
| T-04 | `tests/test_skill_analyzer.py` | `test_invalid_career()` uses a bare `try/except` with `return` to pass — this is an anti-pattern. Should use `pytest.raises`. |
| T-05 | All integration tests | Tests call real CSVs from `data/processed/`. If the processed files are deleted or regenerated differently, tests fail. No fixtures with synthetic data to isolate unit behavior. |
| T-06 | No test | `src/data_preprocessing.py` has no tests at all. |
| T-07 | No test | `src/utils.py` normalize functions have no tests. |
| T-08 | No test | `components/profile_form.py`, `components/dashboard.py`, `components/recommendation_view.py`, `components/learning_path_view.py` have no tests. |

---

## 7. Security and Data Persistence

| # | Issue | Detail |
|---|---|---|
| S-01 | Session-only persistence | All user data (profile, progress, recommendations) lives in `st.session_state`. On browser refresh or server restart, everything is lost. |
| S-02 | No input validation on `name` field | Only `name.strip()` is checked for empty. No length limit or character sanitization. HTML is injected directly: `f"Welcome back, {name} 👋"` — if `name` contained an HTML injection attempt, it would be rendered via `unsafe_allow_html=True`. |
| S-03 | No sanitization of skill text in HTML tags | `dashboard.py` renders `<span class="skill-tag">{skill}</span>` via `unsafe_allow_html=True`. Skills come from the processed CSV (trusted), so this is currently safe, but the pattern is fragile if the skill source were ever user-provided text. |
| S-04 | Hardcoded file paths in tests | Integration tests use the processed CSV at a path relative to the working directory. CI environments with different working directories would fail. |

---

## 8. Hardcoded / Fake Statistics

After inspecting all four component files:

- **Dashboard** — All four metric cards (`coverage`, `matched`, `missing`, `recommendations`) are populated from live computation. ✅ No hardcoded values.
- **Recommendations** — All three metric cards are live. ✅ No hardcoded values.
- **Learning Path** — All three metric cards (`completed_courses`, `progress_percentage`, `remaining_hours`) are computed from session state checkboxes. ✅ No hardcoded values.
- **Recommendation reason** — Generated programmatically from `matched_skills`. ✅ No hardcoded strings.

**Conclusion:** No fake or hardcoded statistics were found in any UI component.

---

## 9. Import and Function Name Consistency

| Symbol | Defined in | Imported by | Status |
|---|---|---|---|
| `load_processed_courses` | `src/data_loader.py` | `skill_analyzer`, `similarity_engine`, `course_recommender`, `learning_path_generator`, `profile_form` | ✅ Consistent |
| `load_processed_career_skills` | `src/data_loader.py` | `skill_analyzer`, `profile_form` | ✅ Consistent |
| `normalize_skill_list` | `src/utils.py` | `skill_analyzer`, `similarity_engine`, `learning_path_generator` | ✅ Consistent |
| `get_personalized_recommendations` | `src/course_recommender.py` | `app.py`, `learning_path_generator` | ✅ Consistent |
| `generate_learning_path` | `src/learning_path_generator.py` | `learning_path_view` | ✅ Consistent |
| `generate_skill_gap_report` | `src/skill_analyzer.py` | `course_recommender` | ✅ Consistent |
| `recommend_courses` | `src/similarity_engine.py` | `course_recommender`, `learning_path_generator` | ✅ Consistent |
| `display_profile_form` | `components/profile_form.py` | `app.py` | ✅ Consistent |
| `display_dashboard` | `components/dashboard.py` | `app.py` | ✅ Consistent |
| `display_recommendations` | `components/recommendation_view.py` | `app.py` | ✅ Consistent |
| `display_learning_path` | `components/learning_path_view.py` | `app.py` | ✅ Consistent |
| `normalize_skill` | `src/data_preprocessing.py` | (only used internally) | ⚠️ Duplicate of `src/utils.py` with smaller alias table |

---

## 10. Files to Preserve (Do Not Delete)

| File | Reason |
|---|---|
| `app.py` | Main entry point; correct structure |
| `components/profile_form.py` | Working form logic |
| `components/dashboard.py` | Working dashboard rendering |
| `components/recommendation_view.py` | Working recommendation display |
| `components/learning_path_view.py` | Working path display (with bugs to fix) |
| `src/data_loader.py` | Correct path resolution |
| `src/skill_analyzer.py` | Fully working |
| `src/similarity_engine.py` | Fully working |
| `src/course_recommender.py` | Fully working |
| `src/learning_path_generator.py` | Fully working |
| `src/utils.py` | Correct canonical skill normalizer |
| `data/raw/courses.csv` | Source dataset |
| `data/raw/career_skills.csv` | Source dataset |
| `data/processed/courses_cleaned.csv` | Processed dataset |
| `data/processed/career_skills_cleaned.csv` | Processed dataset |
| `tests/test_skill_analyzer.py` | Good tests (minor refactor needed) |
| `tests/test_course_recommender.py` | Good tests |
| `tests/test_learning_path.py` | Good tests |
| `tests/test_similarity_engine.py` | Good isolated tests with fixtures |

---

## 11. Files That Need Changes

| File | Changes Required |
|---|---|
| `.streamlit/.streamlit/config.toml` | Move to `.streamlit/config.toml` (fix nested directory) |
| `app.py` | Fix `open_profile` CTA button redirect logic (do not rewrite the file) |
| `src/data_preprocessing.py` | Remove duplicate `if __name__ == "__main__"` blocks and duplicate `pathlib` imports; consider delegating normalization to `src/utils` |
| `components/learning_path_view.py` | Cache learning path result in session state; fix stale progress metrics at top |
| `tests/test_data_loader.py` | Add data loader unit tests |
| `tests/skill_visualization.py` | Rename or move out of `tests/`; add `if __name__ == "__main__"` guard |
| `requirements.txt` | Add `pytest`, `streamlit`, `plotly` with version pins |
| `README.md` | Update with full feature list and instructions |
| `docs/project_overview.md` | Populate with project documentation |
