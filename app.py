import pandas as pd
import streamlit as st

from src.data_cleaning import clean_invalid_records, generate_cleaning_summary
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
from src.crime_trends import (
    prepare_datetime,
    extract_time_features,
    get_monthly_trend,
    generate_trend_summary,
    plot_monthly_trend,
)
from src.offence_analysis import (
    get_offence_distribution_insight,
    prepare_offence_visualization_data,
)
from src.police_division_analysis import (
    calculate_division_crime_counts,
    identify_top_divisions,
    generate_division_rankings,
    create_division_visualization,
    get_division_activity_insight,
)

from src.premises_analysis import (
    group_crimes_by_premises,
    calculate_premises_frequencies,
    identify_top_premises_categories,
    generate_premises_rankings,
    create_premises_visualization,
    get_premises_distribution_insight,
)

from src.hotspot_analysis import (
    process_geographic_coordinates
)

st.title("Toronto Crime Indicators Analytics Tool")

DATASET_PATH = "data/Toronto_Crime_Indicators.csv"


@st.cache_data
def load_and_prepare_data(path: str) -> pd.DataFrame:
    raw_df = load_dataset(path)
    return clean_invalid_records(raw_df)


try:
    df = load_and_prepare_data(DATASET_PATH)

    st.success("Dataset loaded successfully.")
    st.write(f"Total records loaded: {get_record_count(df):,}")

    (
        tab_overview,
        tab_hourly,
        tab_trends,
        tab_neighbourhood,
        tab_offences,
        tab_divisions,
        tab_premises,
        tab_hotspots,
    ) = st.tabs([
        "Overview",
        "Hourly Analysis",
        "Crime Trends",
        "Neighbourhood",
        "Offences",
        "Police Divisions",
        "Premises",
        "Hotspots",
    ])

    with tab_overview:
        st.header("Dataset Preview")
        st.dataframe(df.head())

        st.header("Dataset Quality Validation")
        validation_report = generate_validation_report(df)
        total_missing_values = sum(validation_report["missing_values"].values())

        st.write(f"Total missing values: {total_missing_values}")
        st.write(f"Duplicate records: {validation_report['duplicate_records']}")

        for column, count in validation_report["invalid_date_formats"].items():
            st.write(f"Invalid date formats in {column}: {count}")

        st.header("Data Cleaning Summary")
        st.json(generate_cleaning_summary(df))

    with tab_hourly:
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
            columns=["Hour", "Time Range"],
        )
        st.dataframe(legend_df, use_container_width=True)

        st.subheader("Hourly Crime Visualization")
        fig = create_hourly_crime_visualization(hourly_summary)
        st.pyplot(fig)

    with tab_trends:
        st.header("Crime Trends Over Time")

        trend_df = prepare_datetime(df)
        trend_df = extract_time_features(trend_df)
        monthly_trend = get_monthly_trend(trend_df)
        summary = generate_trend_summary(trend_df)

        st.subheader("Trend Summary")
        st.write(summary["insight"])

        st.subheader("Monthly Trend Table")
        st.dataframe(monthly_trend)

        st.subheader("Monthly Trend Chart")
        fig = plot_monthly_trend(trend_df)
        st.plotly_chart(fig, use_container_width=True)

    with tab_neighbourhood:
        st.header("Crime Analysis by Neighbourhood")

        neighbourhood_df = group_crimes_by_neighbourhood(df)
        st.write(f"Records with valid neighbourhood data: {len(neighbourhood_df):,}")

        neighbourhood_counts = calculate_crime_counts(df)
        top_neighbourhoods = identify_top_crime_neighbourhoods(neighbourhood_counts)
        neighbourhood_rankings = generate_neighbourhood_rankings(top_neighbourhoods)

        st.subheader("Top Neighbourhood Rankings")
        st.dataframe(neighbourhood_rankings)

        st.subheader("Neighbourhood Crime Visualization")
        fig = create_neighbourhood_visualization(neighbourhood_rankings)
        st.pyplot(fig)

    with tab_offences:
        st.header("Offence Type Distribution")

        insight = get_offence_distribution_insight(df)
        st.write(insight["insight"])

        offence_data = prepare_offence_visualization_data(df, top_n=10)
        st.dataframe(offence_data)
        st.bar_chart(offence_data.set_index("OFFENCE")["crime_count"])

    with tab_divisions:
        st.header("Police Division Activity")

        insight = get_division_activity_insight(df)
        st.write(insight["insight"])

        division_counts = calculate_division_crime_counts(df)
        top_divisions = identify_top_divisions(division_counts, top_n=10)
        division_rankings = generate_division_rankings(top_divisions)

        st.subheader("Top Police Divisions")
        st.dataframe(division_rankings)

        st.subheader("Division Crime Visualization")
        fig = create_division_visualization(division_rankings)
        st.pyplot(fig)

    with tab_premises:
        st.header("Premises Type Distribution")

        premises_df = group_crimes_by_premises(df)
        st.write(f"Records with valid premises data: {len(premises_df):,}")

        insight = get_premises_distribution_insight(df)
        st.write(insight["insight"])

        premises_frequencies = calculate_premises_frequencies(df)
        top_premises = identify_top_premises_categories(premises_frequencies, top_n=10)
        premises_rankings = generate_premises_rankings(top_premises)

        st.subheader("Top Premises Categories")
        st.dataframe(premises_rankings)
        
        st.subheader("Premises Distribution Visualization")
        fig = create_premises_visualization(premises_rankings)
        st.pyplot(fig)

    with tab_hotspots:
        st.header("Crime Hotspot Analysis")

        coordinates_df = process_geographic_coordinates(df)

        st.write(f"Valid coordinate records: {len(coordinates_df):,}")

        st.dataframe(coordinates_df.head())

except FileNotFoundError as error:
    st.error(str(error))
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")