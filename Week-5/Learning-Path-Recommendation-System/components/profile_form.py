import streamlit as st

from src.data_loader import (
    load_processed_courses,
    load_processed_career_skills
)


def get_available_skills():

    courses = load_processed_courses()
    career_skills = load_processed_career_skills()

    skills = set()

    for skill_text in courses["skills"].dropna():

        for skill in str(skill_text).split("|"):

            skill = skill.strip()

            if skill:
                skills.add(skill)

    for skill_text in career_skills["required_skills"].dropna():

        for skill in str(skill_text).split("|"):

            skill = skill.strip()

            if skill:
                skills.add(skill)

    return sorted(skills, key=str.casefold)


def display_profile_form():

    career_skills = load_processed_career_skills()

    career_goals = sorted(
        career_skills["career_goal"].dropna().unique().tolist()
    )

    available_skills = get_available_skills()

    st.subheader("Create Your Learning Profile")

    st.write(
        "Enter your current information to get personalized "
        "course recommendations and a learning path."
    )

    with st.form("user_profile_form"):

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name"
        )

        career_goal = st.selectbox(
            "Career Goal",
            career_goals
        )

        current_skills = st.multiselect(
            "Your Current Skills",
            options=available_skills,
            help="Select the skills you already know."
        )

        experience_level = st.selectbox(
            "Experience Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        submitted = st.form_submit_button(
            "Save Profile",
            use_container_width=True
        )

        if submitted:

            if not name.strip():
                st.error("Please enter your name.")

            else:

                profile = {
                    "name": name.strip(),
                    "career_goal": career_goal,
                    "current_skills": current_skills,
                    "experience_level": experience_level
                }

                st.session_state["user_profile"] = profile

                st.success("Your profile has been saved successfully!")

    return st.session_state.get("user_profile")