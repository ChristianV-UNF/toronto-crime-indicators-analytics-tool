import streamlit as st

from src.dashboards.sections.overview import render_overview_section
from src.dashboards.sections.hourly import render_hourly_section
from src.dashboards.sections.trends import render_trends_section
from src.dashboards.sections.neighbourhood import render_neighbourhood_section
from src.dashboards.sections.offences import render_offences_section
from src.dashboards.sections.divisions import render_divisions_section
from src.dashboards.sections.premises import render_premises_section
from src.dashboards.sections.hotspots import render_hotspots_section


DASHBOARD_SECTIONS = [
    "Overview",
    "Hourly Analysis",
    "Crime Trends",
    "Neighbourhood",
    "Offences",
    "Police Divisions",
    "Premises",
    "Hotspots",
]


def render_dashboard_navigation(filtered_df):
    selected_tab = st.radio(
        "Select Dashboard Section",
        DASHBOARD_SECTIONS,
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