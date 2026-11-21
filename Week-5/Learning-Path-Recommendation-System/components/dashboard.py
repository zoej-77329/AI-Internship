import streamlit as st
import pandas as pd


def display_dashboard(profile, result):

    report = result["skill_report"]
    recommendations = result["recommendations"]

    name = profile["name"]
    goal = profile["career_goal"]

    coverage = report["coverage"]
    missing = report["missing_skills"]
    matched = report["matched_skills"]
    uncovered = result["uncovered_skills"]

    st.markdown(
        f"""
        <div class="welcome-banner">
            <div class="welcome-label">YOUR LEARNING OVERVIEW</div>
            <h1>Welcome back, {name} 👋</h1>
            <p>
                Your journey towards becoming a
                <strong>{goal}</strong> starts here.
                Explore your skill gaps and recommended courses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Skill Coverage",
            f"{coverage:.1f}%",
            help="Percentage of required career skills already matched."
        )

    with col2:
        st.metric(
            "Skills Matched",
            len(matched)
        )

    with col3:
        st.metric(
            "Skills to Learn",
            len(missing)
        )

    with col4:
        st.metric(
            "Recommended Courses",
            len(recommendations)
        )

    st.write("")

    # Main dashboard sections
    left, right = st.columns([1.2, 1])

    with left:

        st.markdown(
            '<div class="section-heading">Your Skill Progress</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="custom-card">',
            unsafe_allow_html=True
        )

        st.write("Current career skill coverage")

        st.progress(
            max(0.0, min(float(coverage) / 100, 1.0))
        )

        st.markdown(
            f"""
            <div class="progress-caption">
                <strong>{coverage:.1f}%</strong>
                of required skills matched
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown("**Skills you already have**")

        if matched:
            st.markdown(
                " ".join(
                    f'<span class="skill-tag">{skill}</span>'
                    for skill in matched
                ),
                unsafe_allow_html=True
            )
        else:
            st.info("No required skills matched yet.")

        st.write("")

        st.markdown("**Skills you need to develop**")

        if missing:
            st.markdown(
                " ".join(
                    f'<span class="missing-tag">{skill}</span>'
                    for skill in missing
                ),
                unsafe_allow_html=True
            )
        else:
            st.success("You have matched all listed career skills!")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            '<div class="section-heading">Learning Snapshot</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        st.markdown("**Your learning profile**")

        st.write("🎯 Career goal")
        st.markdown(f"**{goal}**")

        st.divider()

        st.write("📚 Experience level")
        st.markdown(f"**{profile['experience_level']}**")

        st.divider()

        st.write("💡 Current skills")
        st.markdown(f"**{len(profile['current_skills'])} selected skills**")

        st.divider()

        st.write("🧭 Recommendation status")

        if recommendations.empty:
            st.warning("No matching courses found.")
        else:
            st.success(
                f"{len(recommendations)} relevant courses found."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Recommended course preview
    st.markdown(
        '<div class="section-heading">Recommended For You</div>',
        unsafe_allow_html=True
    )

    if recommendations.empty:

        st.info(
            "No matching courses are currently available. "
            "Consider expanding the course dataset."
        )

    else:

        for _, course in recommendations.head(3).iterrows():

            st.markdown('<div class="course-card">', unsafe_allow_html=True)

            st.markdown(
                f"### {course['course_name']}"
            )

            st.caption(
                f"{course['level']}  •  "
                f"{course['duration_hours']} hours"
            )

            st.write(
                "Matched skills: "
                + (
                    ", ".join(course["matched_skills"])
                    if course["matched_skills"]
                    else "Related course content"
                )
            )

            st.progress(
                max(
                    0.0,
                    min(float(course["skill_coverage"]) / 100, 1.0)
                )
            )

            st.caption(
                f"Skill coverage: {course['skill_coverage']:.1f}%"
                f"  |  Ranking score: {course['ranking_score']:.1f}"
            )

            st.markdown("</div>", unsafe_allow_html=True)

    if uncovered:

        st.write("")

        st.warning(
            "Some required skills do not have matching courses "
            "in the current dataset: "
            + ", ".join(uncovered)
        )