import pandas as pd
import streamlit as st

from src.hourly_analysis import (
    group_crimes_by_hour,
    generate_hourly_summary_table,
    create_hourly_crime_visualization,
    identify_peak_hours,
    format_hour_range,
    get_hour_legend,
)


def render_hourly_section(filtered_df):
    st.header("Crime Analysis by Hour of Day")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

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