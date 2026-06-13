import streamlit as st

from src.data_loader import get_record_count


def render_dashboard_metrics(df, dashboard_summary):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", f"{get_record_count(df):,}")

    with col2:
        st.metric("Filtered Records", f"{dashboard_summary['total_records']:,}")

    with col3:
        st.metric("Unique Offences", dashboard_summary["unique_offences"])