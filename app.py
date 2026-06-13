import streamlit as st

from src.data_pipeline import load_clean_validate_dataset
from src.dashboard import get_dashboard_summary
from src.dashboards.sidebar import render_filters, render_export_section
from src.dashboards.metrics import render_dashboard_metrics
from src.dashboards.navigation import render_dashboard_navigation

st.title("Toronto Crime Indicators Analytics Tool")

DATASET_PATH = "data/Toronto_Crime_Indicators.csv"


@st.cache_data
def load_and_prepare_data(path: str) -> dict:
    return load_clean_validate_dataset(path)


try:
    pipeline_result = load_and_prepare_data(DATASET_PATH)
    df = pipeline_result["cleaned_df"]

    filtered_df = render_filters(df)
    dashboard_summary = get_dashboard_summary(filtered_df)

    st.success("Dataset loaded successfully.")

    render_export_section(filtered_df)
    render_dashboard_metrics(df, dashboard_summary)
    render_dashboard_navigation(filtered_df)

except FileNotFoundError as error:
    st.error(str(error))
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")