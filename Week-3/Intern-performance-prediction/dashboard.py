
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# --------------------------------
# Project paths
# --------------------------------

BASE_DIR = Path(__file__).parent

DATA_PATH = BASE_DIR / "dataset" / "intern_performance.csv"
MODEL_PATH = BASE_DIR / "results" / "random_forest_model.pkl"

# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Intern Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Load data and model
# --------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

df = load_data()
model = load_model()

XGB_MODEL_PATH = BASE_DIR / "results" / "xgboost_model.pkl"

xgb_model = joblib.load(XGB_MODEL_PATH)

# Features and target
features = [
    "task_completion_time",
    "feedback_rating",
    "attendance_rate"
]

X = df[features]
y = df["performance_score"]

# Same test split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

predictions = model.predict(X_test)
xgb_predictions = xgb_model.predict(X_test)

# --------------------------------
# Dashboard calculations
# --------------------------------

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

df["Performance Category"] = pd.cut(
    df["performance_score"],
    bins=[-1, 50, 75, 100],
    labels=["Low Performer", "Average Performer", "High Performer"]
)

# --------------------------------
# Sidebar
# --------------------------------

st.sidebar.title("Dashboard Controls")

selected_category = st.sidebar.multiselect(
    "Select Performance Category",
    options=["Low Performer", "Average Performer", "High Performer"],
    default=["Low Performer", "Average Performer", "High Performer"]
)

filtered_df = df[
    df["Performance Category"].isin(selected_category)
]

st.sidebar.markdown("---")
st.sidebar.info("Dataset: 500 Synthetic Intern Records")

# --------------------------------
# Dashboard heading
# --------------------------------

st.title("Intern Performance Dashboard")

st.markdown(
    "Machine Learning based analysis and prediction "
    "of intern performance."
)

st.caption("Dataset contains simulated educational records.")

st.divider()

# --------------------------------
# Performance metrics
# --------------------------------

st.subheader("Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Interns", len(df))
col2.metric("Average Score", f"{df['performance_score'].mean():.2f}")
col3.metric("Average Attendance", f"{df['attendance_rate'].mean():.1f}%")
col4.metric("Average Feedback", f"{df['feedback_rating'].mean():.2f}/5")

st.divider()

# --------------------------------
# Performance categories
# --------------------------------

st.subheader("Intern Performance Categories")

category_counts = (
    filtered_df["Performance Category"]
    .value_counts()
    .reindex(
        ["Low Performer", "Average Performer", "High Performer"],
        fill_value=0
    )
    .reset_index()
)

category_counts.columns = ["Category", "Interns"]

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        category_counts,
        names="Category",
        values="Interns",
        hole=0.45,
        title="Performance Distribution",
        color="Category",
        color_discrete_map={
            "Low Performer": "#E76F51",
            "Average Performer": "#E9C46A",
            "High Performer": "#2A9D8F"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        category_counts,
        x="Category",
        y="Interns",
        color="Category",
        title="Interns by Performance Category",
        text="Interns",
        color_discrete_map={
            "Low Performer": "#E76F51",
            "Average Performer": "#E9C46A",
            "High Performer": "#2A9D8F"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------
# Feature importance
# --------------------------------

st.subheader("Factors Affecting Performance")

importance_df = pd.DataFrame({
    "Feature": [
        "Task Completion Time",
        "Feedback Rating",
        "Attendance Rate"
    ],
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=True)

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Random Forest Feature Importance",
    text=importance_df["Importance"].map(
        lambda x: f"{x * 100:.2f}%"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------
# Attendance vs performance
# --------------------------------

st.subheader("Attendance vs Performance")

fig = px.scatter(
    filtered_df,
    x="attendance_rate",
    y="performance_score",
    color="Performance Category",
    hover_data=["intern_id", "feedback_rating"],
    color_discrete_map={
        "Low Performer": "#E76F51",
        "Average Performer": "#E9C46A",
        "High Performer": "#2A9D8F"
    },
    title="Intern Performance Scatterplot"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# Feedback analysis
# --------------------------------

st.subheader("Feedback Rating Analysis")

fig = px.box(
    filtered_df,
    x="Performance Category",
    y="feedback_rating",
    color="Performance Category",
    title="Feedback Ratings Across Performance Categories"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()


# --------------------------------
# Model Evaluation and Comparison
# --------------------------------

st.subheader("Machine Learning Model Comparison")

comparison_df = pd.read_csv(
    BASE_DIR / "results" / "model_comparison.csv"
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Prediction Error Comparison**")

    error_df = comparison_df.melt(
        id_vars="Model",
        value_vars=["MAE", "RMSE"],
        var_name="Metric",
        value_name="Error"
    )

    fig = px.bar(
        error_df,
        x="Metric",
        y="Error",
        color="Model",
        barmode="group",
        text_auto=".3f",
        title="MAE and RMSE Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**R² Score Comparison**")

    fig = px.bar(
        comparison_df,
        x="Model",
        y="R2 Score",
        color="Model",
        text_auto=".4f",
        title="Model Accuracy Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

best_model = comparison_df.loc[
    comparison_df["R2 Score"].idxmax(), "Model"
]

st.success(f"Best Performing Model: {best_model}")

st.dataframe(
    comparison_df.round(4),
    use_container_width=True,
    hide_index=True
)

# --------------------------------
# Actual vs Predicted
# --------------------------------

st.subheader("Actual vs Predicted Performance")

comparison_predictions = pd.DataFrame({
    "Actual Score": y_test.values,
    "Random Forest": predictions,
    "XGBoost": xgb_predictions
})

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=y_test,
    y=predictions,
    mode="markers",
    name="Random Forest"
))

fig.add_trace(go.Scatter(
    x=y_test,
    y=xgb_predictions,
    mode="markers",
    name="XGBoost"
))

fig.add_trace(go.Scatter(
    x=[0, 100],
    y=[0, 100],
    mode="lines",
    name="Perfect Prediction",
    line=dict(dash="dash")
))

fig.update_layout(
    xaxis_title="Actual Performance Score",
    yaxis_title="Predicted Performance Score"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# Download prediction report
# --------------------------------

report_df = pd.DataFrame({
    "Intern ID": df.loc[X_test.index, "intern_id"].values,
    "Actual Score": y_test.values,
    "Random Forest Prediction": predictions.round(2),
    "XGBoost Prediction": xgb_predictions.round(2)
})

st.download_button(
    label="Download Prediction Report",
    data=report_df.to_csv(index=False),
    file_name="intern_prediction_report.csv",
    mime="text/csv"
)


# --------------------------------
# Individual Intern Prediction
# --------------------------------

st.divider()

st.subheader("Predict Individual Intern Performance")

st.write(
    "Enter intern details to estimate their performance score."
)

with st.form("intern_prediction_form"):

    task_time = st.slider(
        "Task Completion Time (Hours)",
        min_value=1.0,
        max_value=12.0,
        value=5.0,
        step=0.5
    )

    feedback = st.slider(
        "Feedback Rating",
        min_value=1.0,
        max_value=5.0,
        value=3.5,
        step=0.1
    )

    attendance = st.slider(
        "Attendance Rate (%)",
        min_value=60.0,
        max_value=100.0,
        value=90.0,
        step=1.0
    )

    submit = st.form_submit_button(
        "Predict Performance"
    )

if submit:

    input_data = pd.DataFrame({
        "task_completion_time": [task_time],
        "feedback_rating": [feedback],
        "attendance_rate": [attendance]
    })

    rf_score = float(model.predict(input_data)[0])
    xgb_score = float(xgb_model.predict(input_data)[0])

    predicted_score = max(0, min(100, xgb_score))

    if predicted_score <= 50:
        category = "Low Performer"
    elif predicted_score <= 75:
        category = "Average Performer"
    else:
        category = "High Performer"

    st.markdown("### Prediction Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Random Forest",
        f"{rf_score:.2f}/100"
    )

    col2.metric(
        "XGBoost",
        f"{xgb_score:.2f}/100"
    )

    col3.metric(
        "Predicted Performance",
        f"{predicted_score:.2f}/100"
    )

    st.info(f"Predicted Category: {category}")

    st.caption(
        "Prediction generated using the XGBoost model. "
        "This is an estimate based on synthetic training data."
    )

# --------------------------------
# Footer
# --------------------------------

st.markdown("---")

st.caption(
    "Intern Performance Prediction | "
    "Python, Pandas, Scikit-learn, Streamlit and Plotly"
)
