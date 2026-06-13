import streamlit as st

from src.offence_analysis import (
    get_offence_distribution_insight,
    prepare_offence_visualization_data,
)


def render_offences_section(filtered_df):
    st.header("Offence Type Distribution")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

    insight = get_offence_distribution_insight(filtered_df)
    st.write(insight["insight"])

    offence_data = prepare_offence_visualization_data(filtered_df, top_n=10)
    offence_data["OFFENCE"] = offence_data["OFFENCE"].astype(str)

    st.dataframe(offence_data)
    st.bar_chart(offence_data.set_index("OFFENCE")["crime_count"])