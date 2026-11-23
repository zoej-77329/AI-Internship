"""
PathFinder — Learning Path View Component
Visualizes the prerequisite-ordered learning sequence and enables
interactive milestone completion tracking backed by SQLite.
"""

import re
import streamlit as st

from src.learning_path_generator import generate_learning_path
from src.database import (
    mark_course_complete,
    mark_course_incomplete,
    get_completed_courses,
    calculate_progress
)
from components.styles import (
    render_page_header,
    render_skill_badges,
    render_level_badge,
    COLOR_SUCCESS,
    PRIMARY_PURPLE
)


def get_progress_key(career_goal: str, course_id: int) -> str:
    """Generates a stable, scoped session-state key for each course checkbox."""
    sanitized_goal = re.sub(r"[^a-zA-Z0-9]+", "_", str(career_goal).lower())
    return f"completed_{sanitized_goal}_{course_id}"


def _on_checkbox_change(course_id: int, key: str, user_id: int):
    """Callback triggered instantly on checkbox toggle to sync with SQLite database."""
    is_checked = st.session_state.get(key, False)
    if is_checked:
        mark_course_complete(course_id=course_id, user_id=user_id)
    else:
        mark_course_incomplete(course_id=course_id, user_id=user_id)


def display_learning_path(profile):
    """Renders the step-by-step learning roadmap and interactive progress tracker."""
    render_page_header(
        title="Personalized Learning Roadmap",
        subtitle="Step-by-step curriculum sequence with prerequisite dependencies automatically resolved.",
        badge="TOPOLOGICAL ROADMAP"
    )

    user_id = profile.get("user_id", 1)

    # ----------------------------------------------------
    # Generate or Retrieve Cached Learning Path
    # ----------------------------------------------------
    path_cache_key = (
        profile.get("career_goal", ""),
        tuple(sorted(profile.get("current_skills", [])))
    )

    if st.session_state.get("learning_path_key") != path_cache_key:
        try:
            with st.spinner("Resolving course dependencies and constructing roadmap..."):
                result = generate_learning_path(
                    user_skills=profile["current_skills"],
                    career_goal=profile["career_goal"],
                    top_n=5
                )
            st.session_state["learning_path_result"] = result
            st.session_state["learning_path_key"] = path_cache_key
        except Exception as error:
            st.error("Unable to generate your learning roadmap.")
            st.exception(error)
            return
    else:
        result = st.session_state["learning_path_result"]

    path = result["learning_path"]

    if path.empty:
        with st.container(border=True):
            st.warning("No learning path could be generated from the currently available courses.")
            if result.get("unresolved_prerequisites"):
                st.markdown("#### Unresolved Prerequisites")
                for item in result["unresolved_prerequisites"]:
                    st.write(f"• **{item['course']}** requires **{item['missing_prerequisite']}**, but no course in the catalog teaches it.")
        return

    # ----------------------------------------------------
    # Sync SQLite State with Checkbox Keys
    # ----------------------------------------------------
    db_completed = get_completed_courses(user_id=user_id)

    for _, course in path.iterrows():
        cid = int(course["course_id"])
        key = get_progress_key(profile["career_goal"], cid)
        if key not in st.session_state:
            st.session_state[key] = (cid in db_completed)

    # Calculate real-time progress using database helper
    progress_stats = calculate_progress(path, user_id=user_id)
    total_courses = progress_stats["total_courses"]
    completed_courses = progress_stats["completed_courses"]
    progress_percentage = progress_stats["completion_percentage"]
    remaining_courses = progress_stats["remaining_courses"]
    remaining_hours = progress_stats["remaining_hours"]
    total_duration = progress_stats["total_duration"]

    # ----------------------------------------------------
    # Progress Tracker Summary Card
    # ----------------------------------------------------
    with st.container(border=True):
        st.markdown("### Curriculum Progress Tracker")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Courses Completed", f"{completed_courses} / {total_courses}")
        col2.metric("Completion Rate", f"{progress_percentage:.0f}%")
        col3.metric("Remaining Courses", remaining_courses)
        col4.metric("Hours to Goal", f"{remaining_hours:.1f} hrs", help=f"Total path duration: {total_duration:.1f} hours")

        st.write("")
        st.progress(max(0.0, min(progress_percentage / 100.0, 1.0)))

        status_text = (
            f"You have completed **{completed_courses} of {total_courses}** milestone courses "
            f"({progress_percentage:.0f}% completed)."
        )
        st.caption(status_text)

    st.write("")

    # ----------------------------------------------------
    # Step-by-Step Course Roadmap
    # ----------------------------------------------------
    st.markdown("### Sequential Course Steps")
    st.caption("Follow this sequence from first to last. Prerequisite courses appear before the advanced subjects that depend on them.")

    for _, course in path.iterrows():
        course_id = int(course["course_id"])
        step_number = course.get("step", 1)
        key = get_progress_key(profile["career_goal"], course_id)
        completed = st.session_state.get(key, False)

        with st.container(border=True):
            header_col, badge_col = st.columns([3.8, 1.2])

            with header_col:
                if completed:
                    st.markdown(
                        f"<div style='font-size:11px; font-weight:700; color:{COLOR_SUCCESS}; text-transform:uppercase;'>"
                        f"✓ STEP {step_number} &nbsp;•&nbsp; COMPLETED"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"### <span style='color:{COLOR_SUCCESS}'>✓ {course['course_name']}</span> &nbsp; {render_level_badge(course['level'])}",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div style='font-size:11px; font-weight:700; color:{PRIMARY_PURPLE}; text-transform:uppercase;'>"
                        f"STEP {step_number} OF {total_courses}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"### {course['course_name']} &nbsp; {render_level_badge(course['level'])}",
                        unsafe_allow_html=True
                    )

            with badge_col:
                st.markdown(
                    f"<div style='text-align:right; font-size:14px; font-weight:600; color:#202747; margin-top:6px;'>"
                    f"⏱️ {course['duration_hours']} hours"
                    f"</div>",
                    unsafe_allow_html=True
                )

            # Details
            skills_list = course.get("skills", [])
            prereq_list = course.get("prerequisites", [])

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Competencies Acquired**")
                if skills_list:
                    st.markdown(render_skill_badges(skills_list, kind="matched"), unsafe_allow_html=True)
                else:
                    st.caption("No specific skill labels tagged.")

            with c2:
                st.markdown("**Prerequisites Required**")
                if prereq_list:
                    st.markdown(render_skill_badges(prereq_list, kind="missing"), unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<span style='color:#20A67A; font-size:12px; font-weight:600;'>✓ No prerequisites required</span>",
                        unsafe_allow_html=True
                    )

            st.write("")

            # Completion control
            st.checkbox(
                "Mark this course as completed",
                value=completed,
                key=key,
                on_change=_on_checkbox_change,
                args=(course_id, key, user_id)
            )

    st.write("")

    # ----------------------------------------------------
    # Milestone Celebration or Progress Status
    # ----------------------------------------------------
    with st.container(border=True):
        if completed_courses == total_courses and total_courses > 0:
            st.success(
                f"🎉 **Congratulations, {profile.get('name', 'Learner')}!** "
                f"You have marked all {total_courses} courses in your {profile.get('career_goal')} roadmap as completed!"
            )
        elif completed_courses > 0:
            st.info(
                f"🚀 **Great momentum!** You have completed {completed_courses} of {total_courses} courses. "
                f"{remaining_hours:.1f} learning hours remaining until you achieve full role readiness."
            )
        else:
            st.info(
                f"🏁 **Your roadmap is ready.** Begin with **Step 1** to start making progress toward your "
                f"target role as a **{profile.get('career_goal')}**."
            )

    # ----------------------------------------------------
    # Unresolved Prerequisites Section (if any)
    # ----------------------------------------------------
    if result.get("unresolved_prerequisites"):
        st.write("")
        with st.container(border=True):
            st.markdown("#### ⚠️ Prerequisites Requiring Outside Study")
            for item in result["unresolved_prerequisites"]:
                st.warning(
                    f"**{item['course']}** specifies prerequisite skill **{item['missing_prerequisite']}**, "
                    "which currently has no dedicated course in the catalog. Consider independent study for this competency."
                )
