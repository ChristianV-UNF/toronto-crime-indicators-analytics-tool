import streamlit as st

from src.police_division_analysis import (
    calculate_division_crime_counts,
    identify_top_divisions,
    generate_division_rankings,
    create_division_visualization,
    get_division_activity_insight,
)


def render_divisions_section(filtered_df):
    st.header("Police Division Activity")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

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