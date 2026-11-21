"""
PathFinder — Profile Form Component
Manages user profile creation, updating, validation, and persistent storage.
"""

import streamlit as st
from typing import List

from src.data_loader import (
    load_processed_courses,
    load_processed_career_skills
)
from src.database import get_profile, save_profile
from components.styles import (
    render_page_header,
    render_skill_badges
)


def get_available_skills() -> List[str]:
    """Retrieves all unique normalized skills from courses and career paths."""
    courses = load_processed_courses()
    career_skills = load_processed_career_skills()

    skills = set()

    for skill_text in courses["skills"].dropna():
        for skill in str(skill_text).split("|"):
            s = skill.strip()
            if s:
                skills.add(s)

    for skill_text in career_skills["required_skills"].dropna():
        for skill in str(skill_text).split("|"):
            s = skill.strip()
            if s:
                skills.add(s)

    return sorted(skills, key=str.casefold)


def display_profile_form():
    """Renders the comprehensive profile management view."""
    render_page_header(
        title="Your Learning Profile",
        subtitle="Manage your skill inventory and target career role to calibrate personalized recommendations.",
        badge="USER PREFERENCES"
    )

    try:
        career_skills = load_processed_career_skills()
        career_goals = sorted(career_skills["career_goal"].dropna().unique().tolist())
        available_skills = get_available_skills()
    except Exception as e:
        st.error(f"Error loading system profile data: {e}")
        return

    # Load existing profile from session state or persistent SQLite
    saved_profile = st.session_state.get("user_profile")
    if not saved_profile:
        saved_profile = get_profile()
        if saved_profile:
            st.session_state["user_profile"] = saved_profile
        else:
            saved_profile = {}

    user_name = saved_profile.get("name", saved_profile.get("full_name", ""))
    selected_career = saved_profile.get("career_goal", "")
    selected_experience = saved_profile.get("experience_level", "Beginner")
    user_skills = saved_profile.get("current_skills", [])

    # ----------------------------------------------------
    # Active Profile Summary Card (if profile exists)
    # ----------------------------------------------------
    if saved_profile and user_name:
        with st.container(border=True):
            s_col1, s_col2 = st.columns([3, 1])
            with s_col1:
                st.markdown(
                    f"### {user_name} &nbsp; "
                    f"<span style='background:#E6F7F0; color:#1B8A64; font-size:12px; padding:3px 8px; border-radius:6px; font-weight:600;'>Active Profile</span>",
                    unsafe_allow_html=True
                )
                st.caption(
                    f"Target Career: **{selected_career}**  •  "
                    f"Experience: **{selected_experience}**  •  "
                    f"Inventory: **{len(user_skills)} skills registered**"
                )
            with s_col2:
                updated_date = saved_profile.get("updated_at", "")
                if updated_date:
                    short_date = updated_date[:10]
                    st.caption(f"Last updated: **{short_date}**")

            if user_skills:
                st.markdown(render_skill_badges(user_skills, kind="neutral"), unsafe_allow_html=True)

        st.write("")

    # ----------------------------------------------------
    # Profile Edit / Create Form
    # ----------------------------------------------------
    career_index = (
        career_goals.index(selected_career)
        if selected_career in career_goals
        else 0
    )

    experience_options = ["Beginner", "Intermediate", "Advanced"]
    experience_index = (
        experience_options.index(selected_experience)
        if selected_experience in experience_options
        else 0
    )

    with st.container(border=True):
        st.markdown("### Profile Information")
        st.caption("Update your information to automatically recalibrate your course recommendations.")

        with st.form("user_profile_form", clear_on_submit=False):
            f_col1, f_col2 = st.columns(2)

            with f_col1:
                name_input = st.text_input(
                    "Full Name",
                    value=user_name,
                    placeholder="e.g. Alex Morgan",
                    help="Your full name as displayed in the dashboard and certifications."
                )

                experience_input = st.selectbox(
                    "Experience Level",
                    experience_options,
                    index=experience_index,
                    help="Your general professional development level."
                )

            with f_col2:
                career_input = st.selectbox(
                    "Target Career Goal",
                    career_goals,
                    index=career_index,
                    help="The technical profession you want to prepare for."
                )

                st.caption("Selecting a career goal sets the target skill requirements.")

            st.write("")

            skills_input = st.multiselect(
                "Your Current Technical Skills",
                options=available_skills,
                default=[s for s in user_skills if s in available_skills],
                help="Select all technical competencies, programming languages, and tools you have experience with.",
                placeholder="Choose or search your existing skills..."
            )

            st.write("")

            submit_btn = st.form_submit_button(
                "Save & Update Profile",
                type="primary",
                use_container_width=True
            )

            if submit_btn:
                clean_name = name_input.strip()
                if not clean_name:
                    st.error("Please enter a valid full name.")
                elif not career_input:
                    st.error("Please choose a target career goal.")
                else:
                    user_id = saved_profile.get("user_id")
                    persisted = save_profile(
                        full_name=clean_name,
                        career_goal=career_input,
                        current_skills=skills_input,
                        experience_level=experience_input,
                        user_id=user_id
                    )

                    st.session_state["user_profile"] = persisted

                    # Clear cached recommendation & path results to trigger immediate recalculation
                    st.session_state.pop("recommendation_result", None)
                    st.session_state.pop("recommendation_key", None)
                    st.session_state.pop("learning_path_result", None)
                    st.session_state.pop("learning_path_key", None)

                    st.success("✅ Profile successfully saved to persistent storage!")
                    st.rerun()

    return st.session_state.get("user_profile")
