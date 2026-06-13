import streamlit as st

from src.premises_analysis import (
    group_crimes_by_premises,
    calculate_premises_frequencies,
    identify_top_premises_categories,
    generate_premises_rankings,
    create_premises_visualization,
    get_premises_distribution_insight,
)


def render_premises_section(filtered_df):
    st.header("Premises Type Distribution")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

    premises_df = group_crimes_by_premises(filtered_df)
    st.write(f"Records with valid premises data: {len(premises_df):,}")

    insight = get_premises_distribution_insight(filtered_df)
    st.write(insight["insight"])

    premises_frequencies = calculate_premises_frequencies(filtered_df)
    top_premises = identify_top_premises_categories(premises_frequencies, top_n=10)
    premises_rankings = generate_premises_rankings(top_premises)
    premises_rankings["premises_type"] = premises_rankings["premises_type"].astype(str)

    st.subheader("Top Premises Categories")
    st.dataframe(premises_rankings)

    st.subheader("Premises Distribution Visualization")
    if premises_rankings.empty:
        st.info("No premises categories available for the current filter selection.")
    else:
        fig = create_premises_visualization(premises_rankings)
        st.pyplot(fig)