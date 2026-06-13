import pandas as pd
import streamlit as st

from src.data_loader import get_record_count
from src.data_pipeline import load_clean_validate_dataset
from src.dashboard import filter_dataset, get_dashboard_summary
from src.dashbaords.sections.overview import render_overview_section
from src.dashbaords.sections.hourly import render_hourly_section
from src.dashbaords.sections.trends import render_trends_section
from src.dashbaords.sections.neighbourhood import render_neighbourhood_section
from src.dashbaords.sections.offences import render_offences_section
from src.dashbaords.sections.divisions import render_divisions_section
from src.dashbaords.sections.premises import render_premises_section
from src.dashbaords.sections.hotspots import render_hotspots_section
from src.export_result import (
    EXPORT_OPTIONS,
    prepare_export_data,
    convert_dataframe_to_csv,
    generate_export_filename,
    get_export_confirmation_message,
)

st.title("Toronto Crime Indicators Analytics Tool")

DATASET_PATH = "data/Toronto_Crime_Indicators.csv"

@st.cache_data
def load_and_prepare_data(path: str) -> dict:
    return load_clean_validate_dataset(path)

try:
    pipeline_result = load_and_prepare_data(DATASET_PATH)
    df = pipeline_result["cleaned_df"]

    st.sidebar.header("Dashboard Filters")

    available_hours = sorted(df["OCC_HOUR"].dropna().unique().astype(int))
    selected_hours = st.sidebar.multiselect(
        "Filter by Hour",
        available_hours,
        key="hour_filter",
    )

    available_offences = sorted(df["OFFENCE"].dropna().astype(str).unique())
    selected_offences = st.sidebar.multiselect(
        "Filter by Offence",
        available_offences,
        key="offence_filter",
    )

    filtered_df = filter_dataset(
        df,
        selected_hours=selected_hours if selected_hours else None,
        selected_offences=selected_offences if selected_offences else None,
    )

    dashboard_summary = get_dashboard_summary(filtered_df)

    st.success("Dataset loaded successfully.")

    st.sidebar.header("Export Results")

    export_type = st.sidebar.selectbox(
        "Select data to export",
        options=list(EXPORT_OPTIONS.keys()),
        format_func=lambda key: EXPORT_OPTIONS[key],
    )

    prepare_export = st.sidebar.button("Prepare Export")

    if prepare_export:
        try:
            export_df = prepare_export_data(filtered_df, export_type)
            export_filename = generate_export_filename(export_type)
            export_csv = convert_dataframe_to_csv(export_df)

            st.sidebar.download_button(
                label="Download CSV",
                data=export_csv,
                file_name=export_filename,
                mime="text/csv",
            )

            st.sidebar.success(
                get_export_confirmation_message(
                    export_filename,
                    len(export_df),
                )
            )
        except ValueError as error:
            st.sidebar.warning(str(error))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", f"{get_record_count(df):,}")

    with col2:
        st.metric("Filtered Records", f"{dashboard_summary['total_records']:,}")

    with col3:
        st.metric("Unique Offences", dashboard_summary["unique_offences"])

    selected_tab = st.radio(
        "Select Dashboard Section",
        [
            "Overview",
            "Hourly Analysis",
            "Crime Trends",
            "Neighbourhood",
            "Offences",
            "Police Divisions",
            "Premises",
            "Hotspots",
        ],
        horizontal=True,
    )

    if selected_tab == "Overview":
        render_overview_section(filtered_df)
    elif selected_tab == "Hourly Analysis":
        render_hourly_section(filtered_df)
    elif selected_tab == "Crime Trends":
        render_trends_section(filtered_df)
    elif selected_tab == "Neighbourhood":
        render_neighbourhood_section(filtered_df)
    elif selected_tab == "Offences":
        render_offences_section(filtered_df)
    elif selected_tab == "Police Divisions":
        render_divisions_section(filtered_df)
    elif selected_tab == "Premises":
        render_premises_section(filtered_df)
    elif selected_tab == "Hotspots":
        render_hotspots_section(filtered_df)

except FileNotFoundError as error:
    st.error(str(error))
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")