import streamlit as st

from src.crime_trends import (
    prepare_datetime,
    extract_time_features,
    get_monthly_trend,
    generate_trend_summary,
    plot_monthly_trend,
)


def render_trends_section(filtered_df):
    st.header("Crime Trends Over Time")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

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