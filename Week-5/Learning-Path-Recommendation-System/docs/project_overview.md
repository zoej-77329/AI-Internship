# PathFinder — Project Technical Architecture

## 1. Overview
PathFinder is a personalized learning path recommendation platform that connects learner competencies with career requirements through content-based machine learning and topological graph sorting.

---

## 2. Recommendation Algorithm
1. **Canonical Skill Normalization**: Standardizes user inputs and catalog tags against 51 canonical technological definitions (e.g., `NumPy`, `JavaScript`, `OpenCV`, `CI CD`).
2. **Skill Gap Diagnostics**: Computes set intersections and differences between user skills and career benchmarks:
   - $\text{Matched} = \text{User Skills} \cap \text{Required Skills}$
   - $\text{Missing} = \text{Required Skills} \setminus \text{User Skills}$
3. **TF-IDF & Cosine Similarity Vectorization**: Evaluates course corpus against missing competencies query.
4. **Weighted Composite Ranking**:
   $$\text{Score} = 0.70 \times \text{Similarity Score} + 0.30 \times \text{Skill Coverage Score}$$
5. **Prerequisite-Aware Topological Sorting**: Depth-First Search (DFS) with recursive dependency resolution and circular graph detection.

---

## 3. Persistent Storage (SQLite)
- **Database**: `data/pathfinder.db`
- **Tables**: `user_profiles` and `learning_progress`
- Parameterized SQL execution prevents injection and ensures transactional integrity.
