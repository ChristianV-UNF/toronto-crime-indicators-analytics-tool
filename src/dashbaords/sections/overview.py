import streamlit as st

from src.data_cleaning import generate_cleaning_summary
from src.data_validation import generate_validation_report


def render_overview_section(filtered_df):
    st.header("Dataset Preview")
    st.dataframe(filtered_df.head())

    st.header("Dataset Quality Validation")
    validation_report = generate_validation_report(filtered_df)
    total_missing_values = sum(validation_report["missing_values"].values())

    st.write(f"Total missing values: {total_missing_values}")
    st.write(f"Duplicate records: {validation_report['duplicate_records']}")

    for column, count in validation_report["invalid_date_formats"].items():
        st.write(f"Invalid date formats in {column}: {count}")

    st.header("Data Cleaning Summary")
    st.json(generate_cleaning_summary(filtered_df))