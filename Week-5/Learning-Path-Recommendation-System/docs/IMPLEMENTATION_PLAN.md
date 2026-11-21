# PathFinder — Implementation Plan

> Created: 2026-11-21  
> Based on: `docs/PROJECT_AUDIT.md`  
> Rules: Do not rewrite `app.py`; do not delete files; do not replace existing modules; do not generate new datasets; do not install unnecessary packages.

---

## Overview

The project is structurally sound. The core backend (data loading, skill analysis, TF-IDF recommendation, learning path generation) works end-to-end. The remaining work is focused on **five critical/medium bugs**, **test coverage gaps**, **environment setup**, and **documentation**. No new features need to be built from scratch.

```
Phase 1 — Environment & Config Fixes      (immediate blockers)
Phase 2 — UI Bug Fixes                    (user-facing correctness)
Phase 3 — Code Quality & Consistency      (maintainability)
Phase 4 — Test Coverage                   (validation)
Phase 5 — Documentation & Final Polish    (completeness)
```

---

## Phase 1 — Environment & Configuration Fixes

### Objective
Fix the two critical blockers that prevent the app from running correctly: the misplaced Streamlit config file and the missing Python packages.

---

### 1.1 — Fix Streamlit config.toml location

**Problem (BUG-07):** `config.toml` is at `.streamlit/.streamlit/config.toml`. Streamlit expects `.streamlit/config.toml`.

**Files affected:**
- `.streamlit/.streamlit/config.toml` → move content to `.streamlit/config.toml`

**Changes required:**
1. Create `.streamlit/config.toml` at the correct path with the existing content:
   ```toml
   [theme]
   base = "light"
   primaryColor = "#6C63FF"
   backgroundColor = "#F5F6FC"
   secondaryBackgroundColor = "#FFFFFF"
   textColor = "#20243A"
   font = "sans serif"

   [server]
   runOnSave = true
   ```
2. The old `.streamlit/.streamlit/` subfolder can remain (do not delete).

**Tests required:** Manual — run `streamlit run app.py` and confirm the purple accent color and light background are applied from the theme rather than only from injected CSS.

**Expected result:** Streamlit reads the config. Theme colors are consistent. `runOnSave` works during development.

---

### 1.2 — Pin package versions in requirements.txt

**Problem (BUG-11):** `streamlit`, `plotly`, and `pytest` are not installed. Requirements are unpinned.

**Files affected:**
- `requirements.txt`

**Changes required:**
Replace the current 7-line file with pinned versions:
```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
streamlit>=1.35
matplotlib>=3.7
plotly>=5.18
pytest>=8.0
```

**Tests required:** After install, run `python -m pytest tests/ -v` and `streamlit run app.py` to confirm startup.

**Expected result:** All imports succeed. Test runner launches. App renders in browser.

---

## Phase 2 — UI Bug Fixes

### Objective
Fix all user-facing bugs so the app works correctly from first visit through progress tracking.

---

### 2.1 — Fix "Create My Profile" CTA button navigation (BUG-02)

**Problem:** Three buttons in `app.py` set `open_profile=True` and call `st.rerun()`, but `open_profile` is never read to change the navigation page. Users clicking these buttons cannot reach the profile form.

**Files affected:**
- `app.py` (targeted line edits only — do not rewrite the file)

**Changes required:**

The `st.radio` widget must be given a `key` so its value can be overridden from session state. When `open_profile` is `True`, override the radio key to `"My Profile"` before the radio renders.

Specifically, before the `st.radio(...)` call (around Line 362):
```python
# Read the pending navigation request set by CTA buttons
if st.session_state.get("open_profile"):
    st.session_state["nav_page"] = "My Profile"
    st.session_state.pop("open_profile", None)
```

Add `key="nav_page"` and `index` derived from session state to the `st.radio` call:

```python
page = st.radio(
    "NAVIGATION",
    ["Dashboard", "My Profile", "Recommendations", "Learning Path"],
    key="nav_page",
    label_visibility="visible"
)
```

This allows the CTA buttons to work: `st.session_state["nav_page"] = "My Profile"` → `st.rerun()` → radio reads key → page = "My Profile".

**Tests required:**
- Manual test: start app, click "Create My Profile" on the welcome screen → verify navigation switches to "My Profile" page.
- Manual test: click "Create Profile" on Recommendations page → verify navigation to "My Profile".

**Expected result:** All three CTA buttons navigate correctly to the My Profile page.

---

### 2.2 — Cache learning path in session state to prevent regeneration on checkbox toggle (BUG-03)

**Problem:** `generate_learning_path()` is called on every Streamlit rerun inside `display_learning_path()`. Checking a progress checkbox triggers a rerun and re-runs the full TF-IDF pipeline.

**Files affected:**
- `components/learning_path_view.py`

**Changes required:**

Before calling `generate_learning_path()`, check whether a cached result for the current profile already exists in session state:

```python
path_key = ("learning_path_result", profile["career_goal"], tuple(sorted(profile["current_skills"])))

if st.session_state.get("learning_path_key") != path_key:
    with st.spinner("Building your personalized learning path..."):
        result = generate_learning_path(
            user_skills=profile["current_skills"],
            career_goal=profile["career_goal"],
            top_n=5
        )
    st.session_state["learning_path_result"] = result
    st.session_state["learning_path_key"] = path_key
else:
    result = st.session_state["learning_path_result"]
```

The cache is invalidated whenever the career goal or skills change (profile update). This is consistent with how `app.py` caches recommendations.

**Tests required:**
- Manual test: open Learning Path, check a checkbox, verify the path does not re-render/flash and the spinner does not reappear.

**Expected result:** Learning path is generated once per profile state. Checkbox toggles are instant.

---

### 2.3 — Fix stale progress metrics at the top of the learning path page (BUG-04)

**Problem:** `completed_courses` is calculated before `st.checkbox()` widgets are rendered. The top metric cards show the previous rerun's values. (The bottom "Learning Summary" section re-calculates correctly.)

**Files affected:**
- `components/learning_path_view.py`

**Changes required:**

Move the initial progress calculation (Lines 77–104) **below** where the checkpoint keys are established from the path DataFrame, but rely on reading session state before any `st.checkbox()` renders. In Streamlit, `session_state` already reflects the **current** checkbox value at the start of a rerun (the checkbox widget writes its value to session state before the script reruns). The computation is therefore correct — the values just need to be used consistently. The fix is to **share one calculation** between the top metrics and the bottom summary, instead of computing twice:

Replace the two separate `completed_courses` and `progress_percentage` computation blocks with a single helper that reads all checkbox keys from the already-known `path` DataFrame at the top of the render function, after the path is loaded from cache.

**Tests required:**
- Manual test: mark two courses as complete, verify that "Completed Courses: 2/N" appears immediately in the top metrics on the same render.

**Expected result:** Top and bottom progress metrics always show the same value and reflect the current checkbox state.

---

### 2.4 — Fix CSS duplicate rules (BUG-08, UI-03, UI-04, UI-05)

**Problem:** Three CSS selectors are defined twice in `app.py`'s style block. The first definition is dead code.

**Files affected:**
- `app.py` (targeted edit — remove the first/redundant CSS blocks only)

**Changes required:**
- Remove the first `h1, h2, h3` block (Lines 53–56). Keep the fuller `h1, h2, h3, h4` block at Line 293.
- Remove the first `.stButton button` and `.stButton button:hover` block (Lines 207–224). Keep the more complete second block (Lines 248–270) which also styles child `p`, `span`, and `div` elements.
- Merge the two `[data-testid="stVerticalBlockBorderWrapper"]` blocks (Lines 300–306 and Lines 317–319) into one rule that includes all properties: background, border, border-radius, padding, box-shadow, and transition.

**Tests required:**
- Visual review: button text is white and readable; cards have correct border radius and shadow; headings are correct color.

**Expected result:** CSS stylesheet is non-redundant. Browser dev tools show one rule per selector.

---

## Phase 3 — Code Quality & Consistency

### Objective
Eliminate structural debt in `data_preprocessing.py`, fix the misplaced test script, and unify the two normalizer dictionaries.

---

### 3.1 — Clean up `data_preprocessing.py` structural issues (BUG-05)

**Files affected:**
- `src/data_preprocessing.py`

**Changes required:**
1. Remove the duplicate `from pathlib import Path` import (Line 223) and the duplicate `PROJECT_DIR` assignment (Lines 225–226).
2. Merge the three `if __name__ == "__main__":` blocks into one:
   ```python
   if __name__ == "__main__":
       explore_datasets()
       prepare_datasets()
       validate_datasets()
   ```
3. Keep all function definitions intact.

**Tests required:**
- Run `python src/data_preprocessing.py` and verify it executes without errors and prints the validation report.

**Expected result:** Clean, single-entry-point script. No duplicate imports.

---

### 3.2 — Unify skill normalizer dictionaries (BUG-06)

**Files affected:**
- `src/data_preprocessing.py`

**Changes required:**

Replace `data_preprocessing.normalize_skill` with an import from `src/utils.py`:

```python
from src.utils import normalize_skill, normalize_skill_list
```

Remove the local `SKILL_ALIASES` dict and the local `normalize_skill()` and `normalize_skill_column()` function definitions from `data_preprocessing.py`. The existing `normalize_skill_column()` in `data_preprocessing.py` can delegate to `src/utils.normalize_skill_list` if needed.

> [!IMPORTANT]
> `data_preprocessing.py` already imports from `src.data_loader`. Adding an import of `src.utils` is consistent with the existing project pattern and does not create a circular import.

**Tests required:**
- Run `python src/data_preprocessing.py` → verify same output as before.
- Run the existing test suite → all tests pass.

**Expected result:** Single canonical skill normalizer. `prepare_datasets()` and runtime backend use identical normalization logic.

---

### 3.3 — Fix misplaced `tests/skill_visualization.py` (BUG-09)

**Files affected:**
- `tests/skill_visualization.py`

**Changes required:**

Add an `if __name__ == "__main__":` guard so it does not execute when collected by pytest:

```python
if __name__ == "__main__":
    user_skills = ["Python", "Pandas", "NumPy"]
    report = generate_skill_gap_report(user_skills, "AI Engineer")
    matched = len(report["matched_skills"])
    missing = len(report["missing_skills"])
    # ... rest of plot code
    plt.show()
```

This preserves the file (not deleting) and prevents pytest from hanging on `plt.show()`.

**Tests required:**
- Run `python -m pytest tests/ -v` → `skill_visualization.py` is collected but no tests fail.

**Expected result:** Pytest collection succeeds for the entire `tests/` directory.

---

### 3.4 — Fix `recommendation_view.py` course numbering (BUG-07)

**Files affected:**
- `components/recommendation_view.py`

**Changes required:**

Replace `iterrows()` index-based numbering with an explicit rank counter:

```python
for rank, (_, course) in enumerate(recommendations.iterrows(), start=1):
    with st.container(border=True):
        st.markdown(f"### {rank}. {course['course_name']}")
```

**Tests required:** Visual review in the app.

**Expected result:** Courses are always numbered 1, 2, 3 … regardless of internal DataFrame index.

---

## Phase 4 — Test Coverage

### Objective
Achieve meaningful test coverage for all src modules. Fix the empty test file. Ensure tests do not block on external side effects.

---

### 4.1 — Write `tests/test_data_loader.py` (BUG-10 / T-01)

**Files affected:**
- `tests/test_data_loader.py`

**Changes required:**

Add tests covering:
1. `load_courses()` — returns a non-empty DataFrame with the expected 8 columns.
2. `load_career_skills()` — returns a non-empty DataFrame with 3 columns.
3. `load_processed_courses()` — returns a non-empty DataFrame, no missing values in required columns.
4. `load_processed_career_skills()` — returns a non-empty DataFrame.
5. Column name assertions for both raw and processed files.

**Expected result:** `test_data_loader.py` contributes 5+ passing tests.

---

### 4.2 — Write `tests/test_utils.py`

**Files affected:**
- `tests/test_utils.py` (new file)

**Changes required:**

Add tests covering `src/utils.py`:
1. `normalize_skill("python")` → `"Python"`
2. `normalize_skill("NumPy")` → `"NumPy"` (preserved)
3. `normalize_skill("numpy")` → `"NumPy"` (alias resolved)
4. `normalize_skill("github")` → `"GitHub"`
5. `normalize_skill("opencv")` → `"OpenCV"`
6. `normalize_skill("api")` → `"API"`
7. `normalize_skill("ml")` → `"Machine Learning"`
8. `normalize_skill("")` → `""` (empty string)
9. `normalize_skill_list(["python", "ml", "python"])` → `["Python", "Machine Learning"]` (deduplication)

**Expected result:** `test_utils.py` contributes 9+ passing tests covering canonical normalization.

---

### 4.3 — Write `tests/test_data_preprocessing.py`

**Files affected:**
- `tests/test_data_preprocessing.py` (new file)

**Changes required:**

Add tests covering `src/data_preprocessing.py`:
1. `clean_courses()` — drops rows with missing `course_name`, `skills`, `level`, `duration_hours`.
2. `clean_courses()` — drops rows with invalid/non-positive duration.
3. `clean_courses()` — retains only Beginner/Intermediate/Advanced levels.
4. `clean_careers()` — drops rows with missing `career_goal` or `required_skills`.
5. `normalize_skill_column()` — produces pipe-separated normalized skill strings.

Use synthetic DataFrame fixtures (do not read CSVs).

**Expected result:** `test_data_preprocessing.py` contributes 5+ passing tests.

---

### 4.4 — Refactor `test_skill_analyzer.py` to use `pytest.raises` (T-04)

**Files affected:**
- `tests/test_skill_analyzer.py`

**Changes required:**

Replace:
```python
def test_invalid_career():
    try:
        get_career_requirements("Unknown Career")
    except ValueError:
        return
    assert False, "Expected ValueError for invalid career"
```

With:
```python
import pytest

def test_invalid_career():
    with pytest.raises(ValueError):
        get_career_requirements("Unknown Career")
```

**Tests required:** This test itself should still pass.

**Expected result:** Cleaner pytest idiom; failure message is more descriptive.

---

## Phase 5 — Documentation & Final Polish

### Objective
Bring all documentation up to date so the project is complete and self-explanatory.

---

### 5.1 — Update `README.md`

**Files affected:**
- `README.md`

**Changes required:**

Replace the placeholder "Current Progress" section with a full feature description. Add:
- Prerequisites (Python 3.11+)
- Installation: `pip install -r requirements.txt`
- Running the app: `streamlit run app.py`
- Running tests: `python -m pytest tests/ -v`
- Project structure table (all directories and files)
- Feature list (all four pages)
- Known limitations (session-only persistence, 30-course dataset)

---

### 5.2 — Populate `docs/project_overview.md`

**Files affected:**
- `docs/project_overview.md`

**Changes required:**

Add content covering:
- System architecture diagram (text-based)
- Data flow: raw CSVs → preprocessing → processed CSVs → backend modules → Streamlit components
- Module responsibilities table
- Data schema for courses and career_skills
- Key algorithm descriptions (TF-IDF, cosine similarity, prerequisite DFS)

---

### 5.3 — Remove `scratch_audit.py` from project root

**Files affected:**
- `scratch_audit.py` (delete when filesystem permissions allow)

**Changes required:**

This file was created during the audit and should not be part of the project. Delete it, or add `scratch_audit.py` to `.gitignore`.

---

## Summary Table

| Phase | Task | Priority | Files Changed | Effort |
|---|---|---|---|---|
| 1.1 | Fix config.toml location | 🔴 Critical | `.streamlit/config.toml` | 2 min |
| 1.2 | Pin requirements | 🔴 Critical | `requirements.txt` | 5 min |
| 2.1 | Fix CTA button navigation | 🔴 Critical | `app.py` (3 lines) | 15 min |
| 2.2 | Cache learning path in session state | 🔴 Critical | `learning_path_view.py` | 20 min |
| 2.3 | Fix stale progress metrics | 🟡 Medium | `learning_path_view.py` | 15 min |
| 2.4 | Fix duplicate CSS rules | 🟡 Medium | `app.py` | 10 min |
| 3.1 | Clean data_preprocessing.py | 🟡 Medium | `data_preprocessing.py` | 10 min |
| 3.2 | Unify normalizer dictionaries | 🟡 Medium | `data_preprocessing.py` | 10 min |
| 3.3 | Fix misplaced skill_visualization.py | 🟡 Medium | `skill_visualization.py` | 5 min |
| 3.4 | Fix recommendation numbering | 🟢 Low | `recommendation_view.py` | 5 min |
| 4.1 | Write test_data_loader.py | 🟡 Medium | `test_data_loader.py` | 20 min |
| 4.2 | Write test_utils.py | 🟡 Medium | `test_utils.py` (new) | 20 min |
| 4.3 | Write test_data_preprocessing.py | 🟡 Medium | `test_data_preprocessing.py` (new) | 25 min |
| 4.4 | Refactor test_invalid_career | 🟢 Low | `test_skill_analyzer.py` | 5 min |
| 5.1 | Update README.md | 🟢 Low | `README.md` | 20 min |
| 5.2 | Populate project_overview.md | 🟢 Low | `docs/project_overview.md` | 20 min |

**Estimated total implementation time: ~3 hours**

---

## Execution Order

```
Phase 1 → Phase 2 (2.1 → 2.2 → 2.3 → 2.4) → Phase 3 → Phase 4 → Phase 5
```

Phases 1 and 2 must be completed before testing can run and before the app is usable end-to-end. Phases 3–5 can be done in parallel or in any order after Phase 2.
