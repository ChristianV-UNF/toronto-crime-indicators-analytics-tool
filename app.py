import streamlit as st

from src.data_loader import load_dataset
from src.data_loader import get_record_count
from src.data_validation import generate_validation_report


st.title("Toronto Crime Indicators Analytics Tool")

try:
    df = load_dataset("data/Toronto_Crime_Indicators.csv")

    st.success("Dataset loaded successfully.")

    st.write(
        f"Total records loaded: {get_record_count(df):,}"
    )

    st.dataframe(df.head())

    validation_report = generate_validation_report(df)

    st.subheader("Dataset Quality Validation")

    total_missing = sum(
        validation_report["missing_values"].values()
    )

    st.write(f"Total missing values: {total_missing:,}")

    st.write(
        f"Duplicate records: "
        f"{validation_report['duplicate_records']:,}"
    )

    for column, count in validation_report[
        "invalid_date_formats"
    ].items():
        st.write(
            f"Invalid date formats in {column}: {count:,}"
        )

except FileNotFoundError as error:
    st.error(str(error))