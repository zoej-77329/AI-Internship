import streamlit as st

from components.styles import inject_custom_css
from components.profile_form import display_profile_form
from components.dashboard import display_dashboard
from components.course_explorer import display_course_explorer
from components.recommendation_view import display_recommendations
from components.learning_path_view import display_learning_path
from components.about_view import display_about_page

from src.course_recommender import get_personalized_recommendations
from src.database import get_profile


# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PathFinder | Personalized Learning Path Recommendation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject centralized SaaS styling
inject_custom_css()


# ---------------------------------------------------------------------------
# PERSISTENT PROFILE & RECOMMENDATION PIPELINE
# ---------------------------------------------------------------------------
profile = st.session_state.get("user_profile")
if not profile:
    db_profile = get_profile()
    if db_profile:
        st.session_state["user_profile"] = db_profile
        profile = db_profile

if profile and profile.get("career_goal"):
    try:
        profile_key = (
            profile["career_goal"],
            tuple(sorted(profile.get("current_skills", []))),
        )

        if st.session_state.get("recommendation_key") != profile_key:
            with st.spinner("Analyzing your competencies and ranking courses..."):
                result = get_personalized_recommendations(
                    user_skills=profile.get("current_skills", []),
                    career_goal=profile["career_goal"],
                    top_n=5
                )
            st.session_state["recommendation_result"] = result
            st.session_state["recommendation_key"] = profile_key

        result = st.session_state.get("recommendation_result")
    except Exception as error:
        st.error("Unable to generate recommendations.")
        st.exception(error)
        result = None
else:
    result = None


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 15px 0;">
            <div style="font-size: 28px; line-height: 1;">🎯</div>
            <h2 style="color: #FFFFFF; font-size: 22px; font-weight: 800; margin: 4px 0 2px 0;">PathFinder</h2>
            <p style="color: #B9C6E4; font-size: 11.5px; margin: 0; line-height: 1.3;">
                Personalized learning. Clear career direction.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Active Profile Snapshot in Sidebar
    if profile and profile.get("name"):
        p_name = profile.get("name")
        p_goal = profile.get("career_goal", "Career Goal")
        p_lvl = profile.get("experience_level", "Beginner")
        st.markdown(
            f"""
            <div class="sidebar-user-card">
                <h4>{p_name}</h4>
                <p>🎯 {p_goal}</p>
                <p style="font-size: 10.5px; color: #8F9EC4;">Level: {p_lvl}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="sidebar-user-card">
                <h4>Guest Learner</h4>
                <p style="font-size: 11px; color: #8F9EC4;">No profile configured yet</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    nav_options = [
        "Dashboard",
        "My Profile",
        "Course Explorer",
        "Recommendations",
        "Learning Path",
        "About Project"
    ]

    # Handle navigation redirection from CTA buttons
    if st.session_state.pop("open_profile", False):
        st.session_state["nav_selection"] = "My Profile"

    current_nav = st.session_state.get("nav_selection", "Dashboard")
    nav_index = nav_options.index(current_nav) if current_nav in nav_options else 0

    page = st.radio(
        "NAVIGATION",
        nav_options,
        index=nav_index,
        key="nav_selection",
        label_visibility="visible"
    )

    st.divider()

    st.markdown(
        """
        <div style="padding-top: 5px;">
            <p style="color: #8F9EC4; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 700; margin-bottom: 2px;">
                PathFinder Platform
            </p>
            <p style="color: #6C7BA3; font-size: 10.5px; margin: 0;">
                Content-Based Recommendation Engine &bull; Topological Roadmap
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------------------------
if page == "Dashboard":
    if profile and result:
        display_dashboard(profile, result)
    else:
        st.markdown(
            """
            <div class="pf-banner">
                <div class="pf-tagline-badge">PERSONALIZED EDTECH PLATFORM</div>
                <h1>Personalized learning. Clear career direction.</h1>
                <p>
                    Identify your skill gaps, discover relevant verified courses, and follow an 
                    algorithmic, prerequisite-aware roadmap toward your career ambitions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        with st.container(border=True):
            st.markdown("### Start Your Journey")
            st.write(
                "Configure your learning profile to diagnose your competencies, calculate your career readiness, "
                "and generate a personalized learning roadmap."
            )

            if st.button("Create My Learning Profile →", type="primary"):
                st.session_state["open_profile"] = True
                st.rerun()

        st.write("")
        st.markdown("### Platform Capabilities")

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.markdown("#### 🎯 Skill Gap Diagnosis")
                st.write(
                    "Compare your existing skills against industry career benchmarks. "
                    "Discover competencies you've mastered and critical gaps to bridge."
                )

        with c2:
            with st.container(border=True):
                st.markdown("#### 📚 Algorithmic Discovery")
                st.write(
                    "Receive course recommendations ranked using TF-IDF content similarity "
                    "and targeted skill coverage scores."
                )

        with c3:
            with st.container(border=True):
                st.markdown("#### 🧭 Prerequisite Roadmaps")
                st.write(
                    "Follow an ordered learning curriculum with course dependencies resolved, "
                    "persisting your progress safely across sessions."
                )

elif page == "My Profile":
    display_profile_form()

elif page == "Course Explorer":
    display_course_explorer()

elif page == "Recommendations":
    if profile and result:
        display_recommendations(result)
    else:
        st.markdown(
            """
            <div class="pf-banner">
                <div class="pf-tagline-badge">RECOMMENDATIONS</div>
                <h1>Personalized Course Discovery</h1>
                <p>Configure your target career goal and existing skills to unlock algorithmic recommendations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        with st.container(border=True):
            st.info("Please create and save your learning profile first to generate personalized recommendations.")
            if st.button("Set Up Profile →", type="primary"):
                st.session_state["open_profile"] = True
                st.rerun()

elif page == "Learning Path":
    if profile:
        display_learning_path(profile)
    else:
        st.markdown(
            """
            <div class="pf-banner">
                <div class="pf-tagline-badge">LEARNING ROADMAP</div>
                <h1>Sequential Learning Journey</h1>
                <p>Complete courses in an optimal sequence with prerequisites resolved.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        with st.container(border=True):
            st.info("Please create and save your learning profile before viewing your personalized roadmap.")
            if st.button("Set Up Profile →", type="primary"):
                st.session_state["open_profile"] = True
                st.rerun()

elif page == "About Project":
    display_about_page()
