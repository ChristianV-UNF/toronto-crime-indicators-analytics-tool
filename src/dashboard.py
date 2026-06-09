def filter_dataset(
    df,
    selected_hours=None,
    selected_offences=None
):
    filtered_df = df.copy()

    if selected_hours:
        filtered_df = filtered_df[
            filtered_df["OCC_HOUR"].isin(selected_hours)
        ]

    if selected_offences:
        filtered_df = filtered_df[
            filtered_df["OFFENCE"].isin(selected_offences)
        ]

    return filtered_df


def get_dashboard_summary(df):
    return {
        "total_records": len(df),
        "unique_offences": df["OFFENCE"].nunique()
    }