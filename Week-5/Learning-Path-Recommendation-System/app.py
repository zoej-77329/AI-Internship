import streamlit as st

st.set_page_config(
    page_title="Learning Path Recommendation System",
    page_icon="📚",
    layout="wide"
)

st.title("Learning Path Recommendation System")

st.write(
    "Welcome! This application will recommend courses "
    "and generate personalized learning paths based on "
    "your current skills and career goals."
)

st.info("Project setup completed. Recommendation features are coming next.")

st.subheader("Project Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Courses", "30")
col2.metric("Career Paths", "10")
col3.metric("Recommendation Engine", "In Development")