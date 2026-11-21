"""
PathFinder — Dashboard Component
Provides an executive overview of user learning status, skill alignment,
real progress metrics, and recommended courses.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.database import calculate_progress
from src.learning_path_generator import generate_learning_path
from components.styles import (
    render_page_header,
    render_skill_badges,
    render_level_badge,
    get_plotly_theme_defaults,
    COLOR_SUCCESS,
    COLOR_WARNING,
    PRIMARY_PURPLE
)


def display_dashboard(profile, result):
    """Renders the executive dashboard with verified metrics and interactive charts."""
    name = profile.get("name", profile.get("full_name", "Learner"))
    goal = profile.get("career_goal", "Career Goal")
    user_id = profile.get("user_id", 1)

    report = result["skill_report"]
    recommendations = result["recommendations"]

    coverage = float(report.get("coverage", 0.0))
    missing = report.get("missing_skills", [])
    matched = report.get("matched_skills", [])
    uncovered = result.get("uncovered_skills", [])

    # ----------------------------------------------------
    # Real Learning Path & Progress Calculation
    # ----------------------------------------------------
    path_cache_key = (
        profile.get("career_goal", ""),
        tuple(sorted(profile.get("current_skills", [])))
    )

    if st.session_state.get("learning_path_key") != path_cache_key:
        try:
            path_result = generate_learning_path(
                user_skills=profile["current_skills"],
                career_goal=profile["career_goal"],
                top_n=5
            )
            st.session_state["learning_path_result"] = path_result
            st.session_state["learning_path_key"] = path_cache_key
        except Exception:
            path_result = {"learning_path": pd.DataFrame()}
    else:
        path_result = st.session_state.get("learning_path_result", {"learning_path": pd.DataFrame()})

    learning_path_df = path_result.get("learning_path", pd.DataFrame())
    progress_stats = calculate_progress(learning_path_df, user_id=user_id)

    completed_count = progress_stats["completed_courses"]
    total_path_courses = progress_stats["total_courses"]
    path_progress_pct = progress_stats["completion_percentage"]

    # ----------------------------------------------------
    # Header Banner
    # ----------------------------------------------------
    render_page_header(
        title=f"Welcome back, {name}",
        subtitle=f"Target Role: {goal}  •  Experience Level: {profile.get('experience_level', 'Beginner')}",
        badge="DASHBOARD OVERVIEW"
    )

    # ----------------------------------------------------
    # Key Metric Cards (Row 1)
    # ----------------------------------------------------
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.metric(
            label="Skill Match",
            value=f"{coverage:.0f}%",
            help="Percentage of required skills for this role already in your profile."
        )

    with m2:
        st.metric(
            label="Skills Acquired",
            value=f"{len(matched)} / {len(report.get('required_skills', []))}",
            help="Number of core skills already mastered."
        )

    with m3:
        st.metric(
            label="Skills to Learn",
            value=len(missing),
            help="Identified skill gaps required to reach career readiness."
        )

    with m4:
        st.metric(
            label="Target Courses",
            value=len(recommendations),
            help="Relevant courses matched to your skill gaps."
        )

    with m5:
        st.metric(
            label="Path Progress",
            value=f"{completed_count}/{total_path_courses}",
            delta=f"{path_progress_pct:.0f}% Done" if total_path_courses > 0 else None,
            help="Courses completed in your personalized learning roadmap."
        )

    st.write("")

    # ----------------------------------------------------
    # Interactive Visualizations (Row 2)
    # ----------------------------------------------------
    chart_col1, chart_col2 = st.columns([1.1, 1.2])

    with chart_col1:
        with st.container(border=True):
            st.markdown("#### Skill Readiness Breakdown")
            st.caption("Proportion of required career competencies currently mastered.")

            # Donut chart for skill readiness
            donut_data = pd.DataFrame({
                "Status": ["Matched Skills", "Missing Skills"],
                "Count": [max(len(matched), 0), max(len(missing), 0)]
            })

            fig_donut = px.pie(
                donut_data,
                names="Status",
                values="Count",
                hole=0.68,
                color="Status",
                color_discrete_map={
                    "Matched Skills": COLOR_SUCCESS,
                    "Missing Skills": COLOR_WARNING
                }
            )

            layout_defaults = get_plotly_theme_defaults()
            fig_donut.update_layout(
                **layout_defaults,
                height=260,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                annotations=[{
                    "text": f"<b>{coverage:.0f}%</b><br><span style='font-size:11px;color:#737D95'>Match</span>",
                    "x": 0.5, "y": 0.5,
                    "font_size": 22,
                    "showarrow": False
                }]
            )
            fig_donut.update_traces(textinfo="none", hoverinfo="label+value")
            st.plotly_chart(fig_donut, use_container_width=True)

    with chart_col2:
        with st.container(border=True):
            st.markdown("#### Competency Gap Comparison")
            st.caption(f"Skill distribution for {goal}.")

            bar_data = pd.DataFrame({
                "Category": ["Matched", "Gap to Bridge", "Uncovered in Catalog"],
                "Skills Count": [len(matched), len(missing), len(uncovered)],
                "Color": [COLOR_SUCCESS, COLOR_WARNING, "#E56868"]
            })

            fig_bar = px.bar(
                bar_data,
                x="Skills Count",
                y="Category",
                orientation="h",
                text="Skills Count",
                color="Category",
                color_discrete_map={
                    "Matched": COLOR_SUCCESS,
                    "Gap to Bridge": COLOR_WARNING,
                    "Uncovered in Catalog": "#E56868"
                }
            )

            fig_bar.update_layout(
                **layout_defaults,
                height=260,
                showlegend=False,
                xaxis=dict(title="", showgrid=True, gridcolor="#EAEFF8"),
                yaxis=dict(title="", autorange="reversed")
            )
            fig_bar.update_traces(textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

    st.write("")

    # ----------------------------------------------------
    # Detailed Skill Breakdown (Row 3)
    # ----------------------------------------------------
    left_skills, right_skills = st.columns(2)

    with left_skills:
        with st.container(border=True):
            st.markdown(
                f"#### Matched Skills &nbsp; "
                f"<span style='color:{COLOR_SUCCESS}; font-size:13px;'>({len(matched)})</span>",
                unsafe_allow_html=True
            )
            st.caption("Skills you already possess that align with this career goal.")
            if matched:
                st.markdown(render_skill_badges(matched, kind="matched"), unsafe_allow_html=True)
            else:
                st.info("No matching skills identified yet. Start by completing foundational courses.")

    with right_skills:
        with st.container(border=True):
            st.markdown(
                f"#### Skill Gaps to Bridge &nbsp; "
                f"<span style='color:{COLOR_WARNING}; font-size:13px;'>({len(missing)})</span>",
                unsafe_allow_html=True
            )
            st.caption("Key competencies targeted by your personalized course recommendations.")
            if missing:
                st.markdown(render_skill_badges(missing, kind="missing"), unsafe_allow_html=True)
            else:
                st.success("🎉 Outstanding! You have matched all essential skills for this career goal.")

    st.write("")

    # ----------------------------------------------------
    # Top Course Recommendations Preview (Row 4)
    # ----------------------------------------------------
    st.markdown("### Top Recommended Courses")
    st.caption("Highest-scoring courses selected for your career path by algorithmic content matching.")

    if recommendations.empty:
        with st.container(border=True):
            st.info("No course recommendations found matching your current skill gaps.")
    else:
        preview_df = recommendations.head(3)
        cols = st.columns(len(preview_df))

        for idx, (_, course) in enumerate(preview_df.iterrows()):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(
                        f"<div style='font-size:11px; font-weight:700; color:{PRIMARY_PURPLE}; text-transform:uppercase;'>"
                        f"MATCH #{idx + 1}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(f"#### {course['course_name']}")
                    st.markdown(
                        f"{render_level_badge(course['level'])} &nbsp; "
                        f"<span style='font-size:12px; color:#737D95;'>⏱️ {course['duration_hours']} hrs</span>",
                        unsafe_allow_html=True
                    )
                    st.write("")

                    # Scores
                    st.markdown(
                        f"<div style='display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;'>"
                        f"<span>Coverage Score:</span>"
                        f"<strong>{course['skill_coverage']:.0f}%</strong>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.progress(max(0.0, min(float(course["skill_coverage"]) / 100.0, 1.0)))

                    st.caption(
                        f"Relevance: {course['similarity_score']:.0f}%  •  Rank: {course['ranking_score']:.1f}"
                    )

                    st.write("")
                    st.markdown("**Skills Covered:**")
                    st.markdown(
                        render_skill_badges(course["matched_skills"][:3], kind="matched"),
                        unsafe_allow_html=True
                    )

    st.write("")

    # Quick Navigation Callouts
    nav_c1, nav_c2 = st.columns(2)
    with nav_c1:
        if st.button("Explore All Recommendations →", use_container_width=True):
            st.session_state["nav_selection"] = "Recommendations"
            st.rerun()

    with nav_c2:
        if st.button("Open Step-by-Step Roadmap →", use_container_width=True):
            st.session_state["nav_selection"] = "Learning Path"
            st.rerun()
