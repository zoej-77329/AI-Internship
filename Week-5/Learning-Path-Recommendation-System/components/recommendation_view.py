import streamlit as st
import plotly.express as px


def display_recommendations(result):

    report = result["skill_report"]
    recommendations = result["recommendations"]

    st.markdown(
        """
        <div class="page-banner">
            <div class="welcome-label">PERSONALIZED LEARNING</div>
            <h1>Course Recommendations</h1>
            <p>Courses selected based on your career goals and skill gaps.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.metric("Missing Skills", len(report["missing_skills"]))
    col2.metric("Matched Skills", len(report["matched_skills"]))
    col3.metric("Available Courses", len(recommendations))

    st.write("")

    # Skill gap section
    st.markdown("## Your Skill Gap")

    left, right = st.columns(2)

    with left:

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        st.markdown("### <span style='color:#16A085'>Matched Skills</span>",
                    unsafe_allow_html=True)

        for skill in report["matched_skills"]:
            st.markdown(f"✓ {skill}")

        if not report["matched_skills"]:
            st.write("No matched skills.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)

        st.markdown("### <span style='color:#E58A42'>Missing Skills</span>",
                    unsafe_allow_html=True)

        for skill in report["missing_skills"]:
            st.markdown(f"• {skill}")

        if not report["missing_skills"]:
            st.write("No missing skills.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Course recommendations
    st.markdown("## Recommended Courses")

    if recommendations.empty:

        st.info(
            "No matching courses were found for your current skill gaps."
        )

    else:

        for index, course in recommendations.iterrows():

            with st.container(border=True):

                st.markdown(
                    f"### {index + 1}. {course['course_name']}"
                )

                a, b, c = st.columns(3)

                a.metric("Skill Coverage", f"{course['skill_coverage']:.1f}%")
                b.metric("Similarity", f"{course['similarity_score']:.1f}%")
                c.metric("Ranking Score", f"{course['ranking_score']:.1f}")

                st.caption(
                    f"Level: {course['level']}  •  "
                    f"Duration: {course['duration_hours']} hours"
                )

                st.write("**Skills covered**")

                if course["matched_skills"]:
                    st.write(", ".join(course["matched_skills"]))
                else:
                    st.write("No exact missing-skill match.")

                st.info(course["recommendation_reason"])

    # Visual analysis
    st.write("")
    st.markdown("## Recommendation Analysis")

    if not recommendations.empty:

        chart_data = recommendations[
            ["course_name", "skill_coverage", "similarity_score"]
        ].melt(
            id_vars="course_name",
            var_name="Metric",
            value_name="Score"
        )

        fig = px.bar(
            chart_data,
            x="course_name",
            y="Score",
            color="Metric",
            barmode="group",
            title="Course Relevance Comparison",
            color_discrete_sequence=["#6C63FF", "#36B9CC"]
        )

        fig.update_layout(
            template="plotly_white",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=60, b=10),
            legend_title_text=""
        )

        fig.update_xaxes(title="")
        fig.update_yaxes(title="Score (%)", range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

    if result["uncovered_skills"]:

        st.write("")

        st.warning(
            "Courses are not currently available for: "
            + ", ".join(result["uncovered_skills"])
        )