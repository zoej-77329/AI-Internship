import streamlit as st

from components.profile_form import display_profile_form
from components.dashboard import display_dashboard
from components.recommendation_view import display_recommendations
from components.learning_path_view import display_learning_path
from src.course_recommender import get_personalized_recommendations


st.set_page_config(
    page_title="PathFinder | Learning Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------
# CUSTOM DESIGN
# --------------------------------

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #F5F6FC;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #202747 0%, #303D68 100%);
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFF !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.18);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 8px 10px;
        border-radius: 9px;
    }

    h1, h2, h3 {
        color: #20243A;
        font-weight: 750;
    }

    p, label, span {
        color: #49536B;
    }

    .welcome-banner {
        background: linear-gradient(120deg, #5149C9 0%, #7568E9 55%, #8C80F3 100%);
        padding: 36px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 12px 30px rgba(83, 75, 194, 0.18);
    }

    .welcome-banner h1 {
        color: white !important;
        font-size: 34px;
        margin: 12px 0;
    }

    .welcome-banner p {
        color: #F0EFFF !important;
        font-size: 15px;
        max-width: 750px;
    }

    .welcome-banner strong {
        color: white;
    }

    .welcome-label {
        color: #E4E0FF !important;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 700;
    }

    .page-banner {
        background: linear-gradient(120deg, #26395E, #456A94);
        padding: 32px;
        border-radius: 18px;
        color: white;
    }

    .page-banner h1 {
        color: white !important;
        margin-top: 12px;
    }

    .page-banner p {
        color: #E4ECF8 !important;
    }

    .section-heading {
        color: #252C4B;
        font-size: 21px;
        font-weight: 750;
        margin: 15px 0;
    }

    .custom-card {
        background: white;
        padding: 23px;
        border: 1px solid #E8EAF4;
        border-radius: 16px;
        min-height: 250px;
        box-shadow: 0 5px 18px rgba(32, 39, 71, 0.04);
    }

    .course-card {
        background: white;
        padding: 20px;
        margin: 12px 0;
        border: 1px solid #E8EAF4;
        border-left: 4px solid #7568E9;
        border-radius: 14px;
        box-shadow: 0 5px 18px rgba(32, 39, 71, 0.04);
    }

    .course-card h3 {
        font-size: 18px;
    }

    .skill-tag {
        display: inline-block;
        background: #E8F7F2;
        color: #13856A;
        padding: 6px 11px;
        margin: 4px 3px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .missing-tag {
        display: inline-block;
        background: #FFF1E8;
        color: #C66B36;
        padding: 6px 11px;
        margin: 4px 3px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .progress-caption {
        color: #626D84;
        font-size: 13px;
        margin-top: 8px;
    }

    .progress-caption strong {
        color: #6258D7;
        font-size: 22px;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E8EAF4;
        padding: 17px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(32, 39, 71, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #707B91 !important;
    }

    [data-testid="stMetricValue"] {
        color: #252C4B !important;
        font-weight: 750;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: white !important;
        color: #20243A !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextInput"] input {
        border: 1px solid #DDE1EF !important;
        padding: 12px !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #7568E9 !important;
        box-shadow: 0 0 0 2px rgba(117,104,233,0.12);
    }

    .stButton button,
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(100deg, #6258D7, #8174EF);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 650;
        transition: 0.2s;
    }

    .stButton button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background: #5147C2;
        border: none;
        color: white !important;
        box-shadow: 0 5px 15px rgba(98, 88, 215, 0.25);
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #6258D7, #36B9CC);
    }

    [data-testid="stForm"] {
        background: white;
        border: 1px solid #E6E9F3;
        border-radius: 16px;
        padding: 24px;
    }

    [data-testid="stForm"] label {
        color: #303A58 !important;
        font-weight: 600;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    
    /* Fix button text visibility */

    .stButton button {
        background: linear-gradient(110deg, #6258D7, #8174EF) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 11px !important;
        min-height: 46px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
    }

    .stButton button p,
    .stButton button span,
    .stButton button div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stButton button:hover {
        background: #5147C2 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(98, 88, 215, 0.25);
    }

    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(110deg, #6258D7, #8174EF) !important;
        color: #FFFFFF !important;
        min-height: 46px !important;
    }

    [data-testid="stFormSubmitButton"] button p,
    [data-testid="stFormSubmitButton"] button span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Improve page spacing */

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* Improve headings */

    h1, h2, h3, h4 {
        color: #252C4B !important;
        letter-spacing: -0.5px;
    }

    /* Improve card appearance */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E5E8F3 !important;
        border-radius: 17px !important;
        padding: 15px;
        box-shadow: 0 5px 18px rgba(32, 39, 71, 0.045);
    }

    /* Improve navigation buttons */

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 10px;
        padding: 10px;
    }

    /* Learning path improvements */

    [data-testid="stVerticalBlockBorderWrapper"] {
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #B9B2F5 !important;
        box-shadow: 0 8px 22px rgba(98, 88, 215, 0.09);
    }

    [data-testid="stCheckbox"] label {
        color: #303A58 !important;
        font-weight: 600;
    }

    [data-testid="stProgressBar"] {
        border-radius: 20px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 15px 0 25px 0;">
            <div style="font-size:30px;">🎯</div>
            <h2 style="color:white;margin-bottom:2px;">PathFinder</h2>
            <p style="color:#C8D2ED;font-size:12px;">
                Your personalized learning companion
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "My Profile",
        "Recommendations",
        "Learning Path"
    ],
    label_visibility="visible"
    )

    st.divider()

    st.markdown(
        """
        <div style="padding-top:15px;">
            <p style="color:#C8D2ED;font-size:12px;">
                LEARNING PATH RECOMMENDATION SYSTEM
            </p>
            <p style="color:#AEBBDD;font-size:11px;">
                Powered by Python, Scikit-learn and Streamlit
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------
# PROFILE AND RECOMMENDATION DATA
# --------------------------------

profile = st.session_state.get("user_profile")

if profile:

    try:

        profile_key = (
            profile["career_goal"],
            tuple(sorted(profile["current_skills"])),
        )

        if st.session_state.get("recommendation_key") != profile_key:

            with st.spinner("Analyzing your skills and finding relevant courses..."):

                result = get_personalized_recommendations(
                    user_skills=profile["current_skills"],
                    career_goal=profile["career_goal"],
                    top_n=5
                )

            st.session_state["recommendation_result"] = result
            st.session_state["recommendation_key"] = profile_key

        result = st.session_state["recommendation_result"]

    except Exception as error:

        st.error("Unable to generate recommendations.")
        st.exception(error)
        result = None

else:
    result = None


# --------------------------------
# PAGE CONTENT
# --------------------------------

if page == "Dashboard":

    if profile and result:

        display_dashboard(profile, result)

    else:

        st.markdown(
            """
            <div class="welcome-banner">
                <div class="welcome-label">WELCOME TO PATHFINDER</div>
                <h1>Build your next skill.</h1>
                <p>
                    Discover your skill gaps, explore relevant courses,
                    and move closer to your career goals.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown("## Start your learning journey")

        st.write(
            "Create your learning profile to receive personalized "
            "course recommendations and a learning path."
        )

        if st.button("Create My Profile", type="primary"):
            st.session_state["open_profile"] = True
            st.rerun()

        st.markdown("## What PathFinder offers")

        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:
            with st.container(border=True):
                st.markdown("### 🎯")
                st.markdown("#### Skill Analysis")
                st.write(
                    "Identify your existing skills, discover missing "
                    "competencies, and understand your career readiness."
                )
                st.caption("Understand your skill gaps")

        with c2:
            with st.container(border=True):
                st.markdown("### 📚")
                st.markdown("#### Course Discovery")
                st.write(
                    "Discover relevant courses ranked according to "
                    "your career goals and the skills you need."
                )
                st.caption("Find courses that matter")

        with c3:
            with st.container(border=True):
                st.markdown("### 🧭")
                st.markdown("#### Learning Paths")
                st.write(
                    "Follow an organized learning sequence with "
                    "course prerequisites and estimated durations."
                )
                st.caption("Know what to learn next")


elif page == "My Profile":

    st.markdown(
        """
        <div class="page-banner">
            <div class="welcome-label">PERSONAL INFORMATION</div>
            <h1>Your Learning Profile</h1>
            <p>Tell us about your current skills and career ambitions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    display_profile_form()


elif page == "Recommendations":

    if profile and result:

        display_recommendations(result)

    else:

        st.markdown("## Your Recommendations")

        st.info(
            "Create and save your learning profile first to see "
            "personalized recommendations."
        )

        if st.button("Create Profile", type="primary"):
            st.session_state["open_profile"] = True
            st.rerun()

elif page == "Learning Path":

    if profile:

        display_learning_path(profile)

    else:

        st.markdown(
            """
            <div class="page-banner">
                <div class="welcome-label">YOUR PERSONAL ROADMAP</div>
                <h1>Start your learning journey</h1>
                <p>
                    Create your profile before generating
                    your personalized learning path.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button("Create My Profile", type="primary"):

            st.session_state["open_profile"] = True

            st.rerun()