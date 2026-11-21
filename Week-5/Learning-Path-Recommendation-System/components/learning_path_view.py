import streamlit as st
import re

from src.learning_path_generator import generate_learning_path


def get_progress_key(career_goal, course_id):

    goal = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        career_goal.lower()
    )

    return f"completed_{goal}_{course_id}"


def display_learning_path(profile):

    st.markdown(
        """
        <div class="page-banner">
            <div class="welcome-label">YOUR PERSONAL ROADMAP</div>
            <h1>Your Learning Journey 🧭</h1>
            <p>
                Follow your personalized course sequence,
                complete learning milestones, and track your progress.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Generate the actual learning path
    try:

        with st.spinner("Building your personalized learning path..."):

            result = generate_learning_path(
                user_skills=profile["current_skills"],
                career_goal=profile["career_goal"],
                top_n=5
            )

    except Exception as error:

        st.error("Unable to generate your learning path.")
        st.exception(error)
        return

    path = result["learning_path"]

    if path.empty:

        st.warning(
            "No learning path could be generated from the "
            "currently available courses."
        )

        if result["unresolved_prerequisites"]:

            st.markdown("### Prerequisites that need attention")

            for item in result["unresolved_prerequisites"]:

                st.warning(
                    f"{item['course']} requires "
                    f"{item['missing_prerequisite']}, "
                    "but no suitable prerequisite course was found."
                )

        return

    # Calculate current progress
    total_courses = len(path)
    completed_courses = 0

    for _, course in path.iterrows():

        key = get_progress_key(
            profile["career_goal"],
            course["course_id"]
        )

        if st.session_state.get(key, False):
            completed_courses += 1

    progress_percentage = (
        completed_courses / total_courses
    ) * 100

    remaining_hours = sum(
        float(course["duration_hours"])
        for _, course in path.iterrows()
        if not st.session_state.get(
            get_progress_key(
                profile["career_goal"],
                course["course_id"]
            ),
            False
        )
    )

    # Overview metrics
    st.markdown("## Your Progress")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Completed Courses",
        f"{completed_courses}/{total_courses}"
    )

    col2.metric(
        "Overall Progress",
        f"{progress_percentage:.0f}%"
    )

    col3.metric(
        "Hours Remaining",
        f"{remaining_hours:.1f} hrs"
    )

    st.progress(progress_percentage / 100)

    st.caption(
        f"You have completed {completed_courses} "
        f"out of {total_courses} courses."
    )

    st.write("")

    # Learning roadmap
    st.markdown("## Your Course Roadmap")

    st.caption(
        "Complete the courses in the recommended sequence. "
        "Prerequisites are shown on each course."
    )

    for _, course in path.iterrows():

        course_id = course["course_id"]

        key = get_progress_key(
            profile["career_goal"],
            course_id
        )

        completed = st.session_state.get(key, False)

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                if completed:
                    st.markdown(
                        f"### <span style='color:#159B78'>✓ "
                        f"{course['step']}. {course['course_name']}</span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"### {course['step']}. {course['course_name']}"
                    )

            with col2:

                if completed:
                    st.success("Completed")
                else:
                    st.info("Pending")

            a, b = st.columns(2)

            a.caption(f"📊 Level: {course['level']}")
            b.caption(
                f"⏱️ Duration: {course['duration_hours']} hours"
            )

            st.write("**Skills covered**")

            skills = course["skills"]

            if skills:
                st.write(", ".join(skills))
            else:
                st.caption("No skills listed.")

            prerequisites = course["prerequisites"]

            st.write("**Prerequisites**")

            if prerequisites:
                st.write(", ".join(prerequisites))
            else:
                st.caption("No prerequisites listed.")

            st.checkbox(
                "Mark this course as completed",
                key=key
            )

    # Recalculate progress after checkbox changes
    completed_courses = sum(
        bool(
            st.session_state.get(
                get_progress_key(
                    profile["career_goal"],
                    course["course_id"]
                ),
                False
            )
        )
        for _, course in path.iterrows()
    )

    progress_percentage = (
        completed_courses / total_courses
    ) * 100

    st.write("")

    st.markdown("## Learning Summary")

    col1, col2 = st.columns(2)

    col1.metric(
        "Courses Completed",
        completed_courses
    )

    col2.metric(
        "Completion Rate",
        f"{progress_percentage:.1f}%"
    )

    if completed_courses == total_courses:
        st.success(
            "Congratulations! You have marked every course "
            "in this learning path as completed. 🎉"
        )

    elif completed_courses > 0:
        st.info(
            "Great progress! Keep completing your remaining courses."
        )

    else:
        st.info(
            "Your learning journey is ready. Complete your first "
            "course to start tracking your progress."
        )

    # Unresolved prerequisites
    if result["unresolved_prerequisites"]:

        st.write("")

        st.markdown("## Prerequisites Requiring Attention")

        for item in result["unresolved_prerequisites"]:

            st.warning(
                f"{item['course']} requires "
                f"{item['missing_prerequisite']}. "
                "No suitable prerequisite course was found."
            )