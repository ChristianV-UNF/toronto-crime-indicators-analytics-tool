import pandas as pd
import streamlit as st

from src.data_cleaning import generate_cleaning_summary
from src.data_loader import get_record_count
from src.data_validation import generate_validation_report
from src.data_pipeline import load_clean_validate_dataset
from src.dashboard import filter_dataset, get_dashboard_summary
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
    process_geographic_coordinates,
    identify_crime_hotspots,
    highlight_high_density_locations,
    create_hotspot_map_visualization,
)
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

    elif selected_tab == "Hourly Analysis":
        st.header("Crime Analysis by Hour of Day")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            hourly_summary = generate_hourly_summary_table(filtered_df)
            st.subheader("Hourly Crime Summary")
            st.dataframe(hourly_summary)

            hourly_counts = group_crimes_by_hour(filtered_df)
            peak_hours = identify_peak_hours(hourly_counts)

            st.subheader("Peak Crime Hour(s)")
            for hour in peak_hours:
                st.write(f"Hour {hour}: {format_hour_range(hour)}")

            st.subheader("Hour Reference Guide")
            legend_df = pd.DataFrame(
                list(get_hour_legend().items()),
                columns=["Hour", "Time Range"],
            )
            st.dataframe(legend_df, width="stretch")

            st.subheader("Hourly Crime Visualization")
            fig = create_hourly_crime_visualization(hourly_summary)
            st.pyplot(fig)

    elif selected_tab == "Crime Trends":
        st.header("Crime Trends Over Time")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            trend_df = prepare_datetime(filtered_df)
            trend_df = extract_time_features(trend_df)
            monthly_trend = get_monthly_trend(trend_df)
            summary = generate_trend_summary(trend_df)

            st.subheader("Trend Summary")
            st.write(summary["insight"])

            st.subheader("Monthly Trend Table")
            st.dataframe(monthly_trend)

            st.subheader("Monthly Trend Chart")
            fig = plot_monthly_trend(trend_df)
            st.plotly_chart(fig, width="stretch")

    elif selected_tab == "Neighbourhood":
        st.header("Crime Analysis by Neighbourhood")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            neighbourhood_df = group_crimes_by_neighbourhood(filtered_df)
            st.write(f"Records with valid neighbourhood data: {len(neighbourhood_df):,}")

            neighbourhood_counts = calculate_crime_counts(filtered_df)
            top_neighbourhoods = identify_top_crime_neighbourhoods(
                neighbourhood_counts
            )
            neighbourhood_rankings = generate_neighbourhood_rankings(
                top_neighbourhoods
            )

            st.subheader("Top Neighbourhood Rankings")
            st.dataframe(neighbourhood_rankings)

            st.subheader("Neighbourhood Crime Visualization")
            fig = create_neighbourhood_visualization(neighbourhood_rankings)
            st.pyplot(fig)

    elif selected_tab == "Offences":
        st.header("Offence Type Distribution")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            insight = get_offence_distribution_insight(filtered_df)
            st.write(insight["insight"])

            offence_data = prepare_offence_visualization_data(filtered_df, top_n=10)
            offence_data["OFFENCE"] = offence_data["OFFENCE"].astype(str)

            st.dataframe(offence_data)
            st.bar_chart(offence_data.set_index("OFFENCE")["crime_count"])

    elif selected_tab == "Police Divisions":
        st.header("Police Division Activity")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            insight = get_division_activity_insight(filtered_df)
            st.write(insight["insight"])

            division_counts = calculate_division_crime_counts(filtered_df)
            top_divisions = identify_top_divisions(division_counts, top_n=10)
            division_rankings = generate_division_rankings(top_divisions)

            division_rankings["division"] = division_rankings["division"].astype(str)

            st.subheader("Top Police Divisions")
            st.dataframe(division_rankings)

            st.subheader("Division Crime Visualization")
            fig = create_division_visualization(division_rankings)
            st.pyplot(fig)

    elif selected_tab == "Premises":
        st.header("Premises Type Distribution")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            premises_df = group_crimes_by_premises(filtered_df)
            st.write(f"Records with valid premises data: {len(premises_df):,}")

            insight = get_premises_distribution_insight(filtered_df)
            st.write(insight["insight"])

            premises_frequencies = calculate_premises_frequencies(filtered_df)
            top_premises = identify_top_premises_categories(
                premises_frequencies,
                top_n=10,
            )
            premises_rankings = generate_premises_rankings(top_premises)

            premises_rankings["premises_type"] = (
                premises_rankings["premises_type"].astype(str)
            )

            st.subheader("Top Premises Categories")
            st.dataframe(premises_rankings)

            st.subheader("Premises Distribution Visualization")

            if premises_rankings.empty:
                st.info("No premises categories available for the current filter selection.")
            else:
                fig = create_premises_visualization(premises_rankings)
                st.pyplot(fig)

    elif selected_tab == "Hotspots":
        st.header("Crime Hotspot Analysis")

        if filtered_df.empty:
            st.info("No records available for the current filter selection.")
        else:
            coordinates_df = process_geographic_coordinates(filtered_df)
            st.write(f"Valid coordinate records: {len(coordinates_df):,}")

            if coordinates_df.empty:
                st.info("No valid coordinate records found for the current filter selection.")
            else:
                st.dataframe(coordinates_df.head())

                hotspots = identify_crime_hotspots(coordinates_df)

                st.subheader("Top Crime Hotspots")
                st.dataframe(hotspots.head(10))

                high_density_locations = highlight_high_density_locations(hotspots)

                st.subheader("High-Density Crime Locations")
                st.dataframe(high_density_locations)

                st.subheader("Crime Hotspot Map")

                if high_density_locations.empty:
                    st.info(
                        "No high-density crime locations found for the current filter selection."
                    )
                else:
                    high_density_locations = high_density_locations.copy()
                    high_density_locations["LAT_WGS84"] = (
                        high_density_locations["LAT_WGS84"].astype(float)
                    )
                    high_density_locations["LONG_WGS84"] = (
                        high_density_locations["LONG_WGS84"].astype(float)
                    )
                    high_density_locations["crime_count"] = (
                        high_density_locations["crime_count"].astype(int)
                    )

                    hotspot_map = create_hotspot_map_visualization(
                        high_density_locations
                    )
                    st.plotly_chart(hotspot_map, width="stretch")

except FileNotFoundError as error:
    st.error(str(error))
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")