import pandas as pd
import streamlit as st

from src.data_loader import load_dataset, get_record_count
from src.data_validation import generate_validation_report
from src.hourly_analysis import (
    group_crimes_by_hour,
    generate_hourly_summary_table,
    create_hourly_crime_visualization,
    identify_peak_hours,
    format_hour_range,
    get_hour_legend,
)
from src.neighbourhood_analysis import (
    group_crimes_by_neighbourhood,
    calculate_crime_counts,
    identify_top_crime_neighbourhoods,
    generate_neighbourhood_rankings,
    create_neighbourhood_visualization,
)


st.title("Toronto Crime Indicators Analytics Tool")

DATASET_PATH = "data/Toronto_Crime_Indicators.csv"

try:
    df = load_dataset(DATASET_PATH)

    st.success("Dataset loaded successfully.")

    st.write(f"Total records loaded: {get_record_count(df):,}")

    st.dataframe(df.head())

    st.header("Dataset Quality Validation")

    validation_report = generate_validation_report(df)

    total_missing_values = sum(validation_report["missing_values"].values())

    st.write(f"Total missing values: {total_missing_values}")
    st.write(f"Duplicate records: {validation_report['duplicate_records']}")

    for column, count in validation_report["invalid_date_formats"].items():
        st.write(f"Invalid date formats in {column}: {count}")

    st.header("Crime Analysis by Hour of Day")

    hourly_summary = generate_hourly_summary_table(df)

    st.subheader("Hourly Crime Summary")
    st.dataframe(hourly_summary)

    hourly_counts = group_crimes_by_hour(df)
    peak_hours = identify_peak_hours(hourly_counts)

    st.subheader("Peak Crime Hour(s)")
    for hour in peak_hours:
        st.write(f"Hour {hour}: {format_hour_range(hour)}")

    st.subheader("Hour Reference Guide")

    legend_df = pd.DataFrame(
        list(get_hour_legend().items()),
        columns=["Hour", "Time Range"]
    )

    st.dataframe(legend_df, use_container_width=True)

    st.subheader("Hourly Crime Visualization")

    fig = create_hourly_crime_visualization(hourly_summary)
    st.pyplot(fig)

    # Crime Analysis by Neighbourhood
    st.header("Crime Analysis by Neighbourhood")

    neighbourhood_counts = calculate_crime_counts(df)

    top_neighbourhoods = identify_top_crime_neighbourhoods(
        neighbourhood_counts
    )


    neighbourhood_rankings = generate_neighbourhood_rankings(
        top_neighbourhoods
    )

    st.dataframe(neighbourhood_rankings)

    st.subheader("Neighbourhood Crime Visualization")

    fig = create_neighbourhood_visualization(neighbourhood_rankings)
    st.pyplot(fig)


except FileNotFoundError as error:
    st.error(str(error))
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")