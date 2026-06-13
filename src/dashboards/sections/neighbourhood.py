import streamlit as st

from src.neighbourhood_analysis import (
    group_crimes_by_neighbourhood,
    calculate_crime_counts,
    identify_top_crime_neighbourhoods,
    generate_neighbourhood_rankings,
    create_neighbourhood_visualization,
)


def render_neighbourhood_section(filtered_df):
    st.header("Crime Analysis by Neighbourhood")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

    neighbourhood_df = group_crimes_by_neighbourhood(filtered_df)
    st.write(f"Records with valid neighbourhood data: {len(neighbourhood_df):,}")

    neighbourhood_counts = calculate_crime_counts(filtered_df)
    top_neighbourhoods = identify_top_crime_neighbourhoods(neighbourhood_counts)
    neighbourhood_rankings = generate_neighbourhood_rankings(top_neighbourhoods)

    st.subheader("Top Neighbourhood Rankings")
    st.dataframe(neighbourhood_rankings)

    st.subheader("Neighbourhood Crime Visualization")
    fig = create_neighbourhood_visualization(neighbourhood_rankings)
    st.pyplot(fig)