"""
PathFinder — Recommendation View Component
Presents ranked course recommendations based on TF-IDF semantic similarity
and target skill gap coverage.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List

from components.styles import (
    render_page_header,
    render_skill_badges,
    render_level_badge,
    get_plotly_theme_defaults,
    PRIMARY_PURPLE,
    COLOR_SUCCESS
)


def split_pipe(val) -> List[str]:
    """Helper to split pipe-separated strings into cleaned lists."""
    if pd.isna(val) or not str(val).strip():
        return []
    return [s.strip() for s in str(val).split("|") if s.strip()]


def display_recommendations(result):
    """Renders personalized course recommendations with comparative analytics."""
    render_page_header(
        title="Course Recommendations",
        subtitle="Algorithmic recommendations ranked by content similarity and targeted skill gap coverage.",
        badge="CONTENT-BASED ENGINE"
    )

    report = result["skill_report"]
    recommendations = result["recommendations"]
    uncovered = result.get("uncovered_skills", [])

    # ----------------------------------------------------
    # Summary Metrics Row
    # ----------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Missing Skills Identified", len(report.get("missing_skills", [])))
    m2.metric("Skills Already Mastered", len(report.get("matched_skills", [])))
    m3.metric("Recommended Courses", len(recommendations))
    top_score = f"{recommendations.iloc[0]['ranking_score']:.1f}" if not recommendations.empty else "N/A"
    m4.metric("Top Recommendation Score", top_score)

    st.write("")

    # ----------------------------------------------------
    # Algorithmic Notice Callout
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown(
            "ℹ️ **Algorithmic Scoring Notice**: "
            "Scores represent TF-IDF cosine similarity and skill coverage percentages measuring topical "
            "and competency alignment. They are mathematical relevance indicators, not probabilistic forecasts of academic success."
        )

    st.write("")

    # ----------------------------------------------------
    # Comparative Visual Analysis
    # ----------------------------------------------------
    if not recommendations.empty:
        with st.container(border=True):
            st.markdown("### Comparative Course Relevance")
            st.caption("Visual comparison of skill coverage and TF-IDF semantic similarity across recommended courses.")

            chart_data = recommendations[
                ["course_name", "skill_coverage", "similarity_score"]
            ].melt(
                id_vars="course_name",
                var_name="Metric",
                value_name="Score"
            )
            chart_data["Metric"] = chart_data["Metric"].replace({
                "skill_coverage": "Skill Coverage (%)",
                "similarity_score": "Content Similarity (%)"
            })

            fig = px.bar(
                chart_data,
                x="course_name",
                y="Score",
                color="Metric",
                barmode="group",
                color_discrete_map={
                    "Skill Coverage (%)": COLOR_SUCCESS,
                    "Content Similarity (%)": PRIMARY_PURPLE
                }
            )

            layout_defaults = get_plotly_theme_defaults()
            fig.update_layout(
                **layout_defaults,
                height=320,
                xaxis=dict(title="", tickangle=-10),
                yaxis=dict(title="Score (%)", range=[0, 105], showgrid=True, gridcolor="#EAEFF8"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig.update_traces(texttemplate="%{y:.0f}%", textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

    st.write("")

    # ----------------------------------------------------
    # Ranked Course Cards
    # ----------------------------------------------------
    st.markdown("### Ranked Recommendations")
    st.caption("Review each course's relevance score breakdown, covered competencies, and prerequisites.")

    if recommendations.empty:
        with st.container(border=True):
            st.info("No matching courses were found for your current skill gaps.")
            st.caption("Your existing skills may already cover all required competencies, or the catalog may not have corresponding courses.")
        return

    for rank, (_, course) in enumerate(recommendations.iterrows(), start=1):
        with st.container(border=True):
            top_col, meta_col = st.columns([3.5, 1.2])

            with top_col:
                st.markdown(
                    f"<div style='font-size:11px; font-weight:700; color:{PRIMARY_PURPLE}; text-transform:uppercase;'>"
                    f"RANK #{rank} &nbsp;•&nbsp; COMPOSITE SCORE: {course['ranking_score']:.1f}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"### {course['course_name']} &nbsp; {render_level_badge(course['level'])}",
                    unsafe_allow_html=True
                )

            with meta_col:
                st.markdown(
                    f"<div style='text-align:right; font-size:13.5px; font-weight:600; color:#202747; margin-top:6px;'>"
                    f"⏱️ {course['duration_hours']} hours"
                    f"</div>",
                    unsafe_allow_html=True
                )

            # Course description
            if "description" in course and pd.notna(course["description"]):
                st.write(course["description"])

            # Score Breakdown Metrics
            s1, s2, s3 = st.columns(3)
            s1.metric("Skill Coverage", f"{course['skill_coverage']:.1f}%")
            s2.metric("Content Similarity", f"{course['similarity_score']:.1f}%")
            s3.metric("Ranking Score", f"{course['ranking_score']:.1f}")

            st.write("")

            # Competencies row
            c_left, c_right = st.columns(2)
            with c_left:
                st.markdown("**Competencies Addressed**")
                matched_k = course.get("matched_skills", [])
                if matched_k:
                    st.markdown(render_skill_badges(matched_k, kind="matched"), unsafe_allow_html=True)
                else:
                    st.caption("Related content alignment (no exact missing-skill label match)")

            with c_right:
                st.markdown("**All Course Skills**")
                course_all_skills = split_pipe(course.get("skills", ""))
                st.markdown(render_skill_badges(course_all_skills, kind="neutral"), unsafe_allow_html=True)

            st.write("")

            # Recommendation reason callout
            reason = course.get("recommendation_reason", "")
            if reason:
                st.markdown(
                    f"<div style='background:#F4F6FC; border-left:3px solid {PRIMARY_PURPLE}; padding:8px 12px; border-radius:6px; font-size:13px; color:#252C4B;'>"
                    f"<strong>Why this course:</strong> {reason}"
                    f"</div>",
                    unsafe_allow_html=True
                )

    # ----------------------------------------------------
    # Uncovered Skills Notification
    # ----------------------------------------------------
    if uncovered:
        st.write("")
        with st.container(border=True):
            st.warning(
                "Some required skills do not have matching courses in the current catalog: "
                + ", ".join(uncovered)
            )
            st.caption("Consider supplementing your curriculum with self-study or external resources for these topics.")
