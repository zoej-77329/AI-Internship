"""
PathFinder — About Project Component
Presents system architecture, recommendation methodology, technology stack, and objectives.
"""

import streamlit as st
from components.styles import render_page_header


def display_about_page():
    """Renders the About Project view with comprehensive system documentation."""
    render_page_header(
        title="About PathFinder",
        subtitle="Personalized learning path recommendation system powered by content-based filtering, graph sequencing, and skill gap analytics.",
        badge="SYSTEM ARCHITECTURE & METHODOLOGY"
    )

    # ----------------------------------------------------
    # Problem Statement & Overview
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🎯 Project Overview & Problem Statement")
        st.write(
            "In modern software and data industries, aspiring engineers face an overwhelming volume of "
            "online courses with unclear dependencies, redundant content, and inconsistent terminology. "
            "Learners often spend hundreds of hours studying topics they already know or taking advanced courses "
            "without having fulfilled foundational prerequisites."
        )
        st.write(
            "**PathFinder** solves this challenge by performing automated skill gap analysis against targeted career roles, "
            "matching relevant courses through TF-IDF content similarity and skill coverage heuristics, and constructing an "
            "ordered, prerequisite-aware learning roadmap."
        )

    st.write("")

    # ----------------------------------------------------
    # Core Objectives
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🧭 Core Objectives")
        o1, o2 = st.columns(2)
        with o1:
            st.markdown(
                """
                - **Skill Gap Diagnosis**: Compare user-declared proficiencies against curated industry career profiles.
                - **Algorithmic Course Discovery**: Rank learning material using dual-metric TF-IDF cosine similarity and skill coverage.
                """
            )
        with o2:
            st.markdown(
                """
                - **Prerequisite-Aware Sequencing**: Perform cycle-detected topological path generation so learners never skip foundations.
                - **Persistent Progress Tracking**: Maintain SQLite-backed learning states across browser sessions and reloads.
                """
            )

    st.write("")

    # ----------------------------------------------------
    # Recommendation Methodology
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### 🧠 Recommendation Engine Methodology")
        st.write(
            "PathFinder implements a two-stage recommendation and sequencing pipeline:"
        )

        st.markdown(
            """
            1. **Skill Normalization & Gap Analysis**:
               Input user skills and career requirements are normalized using a 51-term canonical alias dictionary 
               (e.g., standardizing `js` → `JavaScript`, `ml` → `Machine Learning`, preserving casing for `NumPy` and `OpenCV`).
               The system computes $S_{\\text{matched}} = S_{\\text{user}} \\cap S_{\\text{required}}$ and $S_{\\text{missing}} = S_{\\text{required}} \\setminus S_{\\text{user}}$.

            2. **TF-IDF Vectorization & Cosine Similarity**:
               Course textual content (combining course title, description, and tagged competencies) is transformed into 
               a TF-IDF vector space ($n$-gram range: 1–2, english stop words removed). The user's missing skills form the query vector:
               $$\\text{Similarity}(u, c) = \\frac{\\mathbf{v}_u \\cdot \\mathbf{v}_c}{\\|\\mathbf{v}_u\\| \\|\\mathbf{v}_c\\|} \\times 100$$

            3. **Composite Ranking Formula**:
               Courses are ranked by a linear combination prioritizing semantic relevance with direct skill coverage:
               $$\\text{Ranking Score} = 0.70 \\times \\text{Similarity Score} + 0.30 \\times \\text{Skill Coverage Score}$$

            4. **Prerequisite Resolution via Topological Graph Search**:
               Target recommended courses undergo recursive dependency resolution using depth-first search (DFS) 
               with cycle detection (`visiting_courses` stack). When a course requires missing prerequisite skills, 
               the engine resolves and prepends the highest-ranked prerequisite course before the target course.
            """
        )

    st.write("")

    # ----------------------------------------------------
    # Technology Stack
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### 💻 Technology Stack")

        t1, t2, t3, t4 = st.columns(4)
        with t1:
            st.markdown("**Core Runtime**")
            st.caption("Python 3.11\nStandard Library\npathlib & sqlite3")
        with t2:
            st.markdown("**Data Science & ML**")
            st.caption("Scikit-Learn (TF-IDF)\nPandas 2.x\nNumPy 2.x")
        with t3:
            st.markdown("**UI & Analytics**")
            st.caption("Streamlit 1.35+\nPlotly Express\nCustom Modern CSS")
        with t4:
            st.markdown("**Quality Assurance**")
            st.caption("Pytest Suite\n35 Unit & Integration Tests\nCI-ready fixtures")

    st.write("")

    # ----------------------------------------------------
    # Limitations & Design Scope
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### ⚠️ Dataset Scope & System Limitations")
        st.markdown(
            """
            - **Curated Dataset Scope**: The system utilizes a curated catalog of 30 representative foundational and intermediate courses across 10 industry career goals.
            - **Heuristic Duration Estimates**: Course duration values represent structured completion times rather than dynamic pacing models.
            - **Content-Based Filtering**: The recommender uses strictly verified course competencies and descriptions without relying on synthetic or unverified student review ratings.
            """
        )
