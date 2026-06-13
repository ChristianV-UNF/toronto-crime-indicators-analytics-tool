import streamlit as st

from src.dashboard import filter_dataset
from src.export_result import (
    EXPORT_OPTIONS,
    prepare_export_data,
    convert_dataframe_to_csv,
    generate_export_filename,
    get_export_confirmation_message,
)


def render_filters(df):
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

    return filter_dataset(
        df,
        selected_hours=selected_hours if selected_hours else None,
        selected_offences=selected_offences if selected_offences else None,
    )


def render_export_section(filtered_df):
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