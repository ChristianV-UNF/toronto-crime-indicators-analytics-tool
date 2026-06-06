import pandas as pd


def validate_offence_column(df):
    if "OFFENCE" not in df.columns:
        raise ValueError("OFFENCE column is missing from the dataset.")

    if df.empty:
        raise ValueError("Dataset is empty.")


def analyze_offence_distribution(df):
    validate_offence_column(df)

    offence_distribution = (
        df["OFFENCE"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("OFFENCE")
        .reset_index(name="crime_count")
    )

    total_crimes = offence_distribution["crime_count"].sum()

    offence_distribution["percentage"] = (
        offence_distribution["crime_count"] / total_crimes * 100
    ).round(2)

    return offence_distribution


def get_most_frequent_offences(df, top_n=10):
    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    offence_distribution = analyze_offence_distribution(df)

    return offence_distribution.head(top_n)


def get_top_offence_summary(df):
    offence_distribution = analyze_offence_distribution(df)

    top_offence = offence_distribution.iloc[0]

    return {
        "most_frequent_offence": top_offence["OFFENCE"],
        "crime_count": int(top_offence["crime_count"]),
        "percentage": float(top_offence["percentage"]),
    }


def prepare_offence_visualization_data(df, top_n=10):
    top_offences = get_most_frequent_offences(df, top_n)

    return top_offences[["OFFENCE", "crime_count", "percentage"]]
def get_offence_distribution_insight(df):
    summary = get_top_offence_summary(df)

    return {
        "insight": (
            f"The most frequent offence is {summary['most_frequent_offence']} "
            f"with {summary['crime_count']} reported crimes, "
            f"representing {summary['percentage']}% of all offences."
        )
    }