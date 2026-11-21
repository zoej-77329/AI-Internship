"""
PathFinder — Course Explorer Component
Allows users to search, filter, sort, and inspect courses in the catalog.
"""

import streamlit as st
import pandas as pd
from typing import List

from src.data_loader import load_processed_courses
from components.styles import (
    render_page_header,
    render_skill_badges,
    render_level_badge
)


def split_pipe(val) -> List[str]:
    """Helper to split pipe-separated strings into cleaned lists."""
    if pd.isna(val) or not str(val).strip():
        return []
    return [s.strip() for s in str(val).split("|") if s.strip()]


def display_course_explorer():
    """Renders the Course Explorer catalog view with interactive filters."""
    render_page_header(
        title="Course Explorer",
        subtitle="Search, filter, and inspect verified courses across foundational and advanced technical domains.",
        badge="CURATED CATALOG"
    )

    try:
        courses = load_processed_courses()
    except Exception as e:
        st.error(f"Unable to load course data: {e}")
        return

    if courses.empty:
        st.warning("No courses are currently available in the catalog.")
        return

    # Extract filter options
    categories = sorted(courses["category"].dropna().unique().tolist())
    all_skills = set()
    for s in courses["skills"].dropna():
        for skill in split_pipe(s):
            all_skills.add(skill)
    sorted_skills = sorted(all_skills, key=str.casefold)

    # ----------------------------------------------------
    # Filter Toolbar
    # ----------------------------------------------------
    with st.container(border=True):
        search_query = st.text_input(
            "Search Courses",
            placeholder="Search by course title or keyword (e.g. Python, Machine Learning, Docker)...",
            label_visibility="collapsed"
        )

        f_col1, f_col2, f_col3, f_col4 = st.columns([1.2, 1.2, 1.6, 1.2])

        with f_col1:
            level_options = ["All Levels", "Beginner", "Intermediate", "Advanced"]
            selected_level = st.selectbox("Difficulty Level", level_options, index=0)

        with f_col2:
            cat_options = ["All Categories"] + categories
            selected_category = st.selectbox("Domain Category", cat_options, index=0)

        with f_col3:
            selected_skills = st.multiselect(
                "Filter by Skills",
                options=sorted_skills,
                placeholder="Choose skills..."
            )

        with f_col4:
            sort_options = [
                "Default (Course ID)",
                "Duration (Low to High)",
                "Duration (High to Low)",
                "Course Name (A-Z)"
            ]
            selected_sort = st.selectbox("Sort By", sort_options, index=0)

    # ----------------------------------------------------
    # Apply Filtering
    # ----------------------------------------------------
    filtered = courses.copy()

    # Text search
    if search_query.strip():
        q = search_query.strip().casefold()
        filtered = filtered[
            filtered["course_name"].str.casefold().str.contains(q, na=False) |
            filtered["description"].str.casefold().str.contains(q, na=False) |
            filtered["skills"].str.casefold().str.contains(q, na=False)
        ]

    # Level filter
    if selected_level != "All Levels":
        filtered = filtered[filtered["level"].str.casefold() == selected_level.casefold()]

    # Category filter
    if selected_category != "All Categories":
        filtered = filtered[filtered["category"].str.casefold() == selected_category.casefold()]

    # Skills filter (course must match at least one selected skill)
    if selected_skills:
        chosen_set = {s.casefold() for s in selected_skills}
        filtered = filtered[
            filtered["skills"].apply(
                lambda val: any(s.casefold() in chosen_set for s in split_pipe(val))
            )
        ]

    # Sorting
    if selected_sort == "Duration (Low to High)":
        filtered = filtered.sort_values(by=["duration_hours", "course_name"], ascending=[True, True])
    elif selected_sort == "Duration (High to Low)":
        filtered = filtered.sort_values(by=["duration_hours", "course_name"], ascending=[False, True])
    elif selected_sort == "Course Name (A-Z)":
        filtered = filtered.sort_values(by="course_name", ascending=True)
    else:
        filtered = filtered.sort_values(by="course_id", ascending=True)

    # Summary metrics header
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Matching Courses", len(filtered))
    m_col2.metric("Total Catalog Hours", f"{filtered['duration_hours'].sum():.0f} hrs")
    m_col3.metric("Available Domains", len(filtered["category"].unique()))

    st.write("")

    # ----------------------------------------------------
    # Course Cards Display
    # ----------------------------------------------------
    if filtered.empty:
        with st.container(border=True):
            st.info("🔍 No courses match your selected search criteria or filters.")
            st.caption("Try removing some filters or searching for a broader term like 'Python' or 'Data'.")
        return

    st.caption(f"Showing **{len(filtered)}** of **{len(courses)}** verified courses")

    for _, row in filtered.iterrows():
        with st.container(border=True):
            header_col, meta_col = st.columns([3.5, 1.2])

            with header_col:
                st.markdown(
                    f"### {row['course_name']} &nbsp; {render_level_badge(row['level'])}",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<span style='color:#737D95; font-size:13px;'>Category: <strong>{row['category']}</strong></span>",
                    unsafe_allow_html=True
                )

            with meta_col:
                st.markdown(
                    f"<div style='text-align:right; font-size:14px; font-weight:600; color:#202747;'>"
                    f"⏱️ {row['duration_hours']} hours"
                    f"</div>",
                    unsafe_allow_html=True
                )

            st.write(row["description"])

            skills_list = split_pipe(row.get("skills", ""))
            prereq_list = split_pipe(row.get("prerequisites", ""))

            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown("**Skills Acquired**")
                st.markdown(render_skill_badges(skills_list, kind="matched"), unsafe_allow_html=True)

            with c2:
                st.markdown("**Prerequisites**")
                if prereq_list:
                    st.markdown(render_skill_badges(prereq_list, kind="missing"), unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<span style='color:#20A67A; font-size:12.5px; font-weight:600;'>✓ None (Beginner Friendly)</span>",
                        unsafe_allow_html=True
                    )
