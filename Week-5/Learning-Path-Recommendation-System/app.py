import streamlit as st

from components.profile_form import display_profile_form


st.set_page_config(
    page_title="Learning Path Recommendation System",
    page_icon="📚",
    layout="wide"
)


st.title("Learning Path Recommendation System")

st.write(
    "Get personalized course recommendations and build "
    "a learning path based on your skills and career goals."
)

st.divider()

profile = display_profile_form()

if profile:

    st.divider()

    st.subheader("Your Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Career Goal", profile["career_goal"])
        st.metric("Experience Level", profile["experience_level"])

    with col2:
        st.metric("Selected Skills", len(profile["current_skills"]))

    st.write("**Name:**", profile["name"])

    st.write("**Current Skills:**")

    if profile["current_skills"]:
        st.write(", ".join(profile["current_skills"]))
    else:
        st.info("No existing skills selected.")

    st.info(
        "Your profile is ready. Personalized recommendations "
        "will be connected in the next development stage."
    )

else:

    st.info("Complete the form above to create your learning profile.")