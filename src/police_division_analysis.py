import pandas as pd
import matplotlib.pyplot as plt


def group_crimes_by_division(df, division_column="DIVISION"):
    if division_column not in df.columns:
        raise KeyError(f"{division_column} column not found")

    division_df = df[[division_column]].copy()
    division_df = division_df.dropna()

    return division_df


def calculate_division_crime_counts(df, division_column="DIVISION"):
    division_df = group_crimes_by_division(df, division_column)

    division_counts = (
        division_df[division_column]
        .value_counts()
        .sort_values(ascending=False)
    )

    return division_counts


def identify_top_divisions(division_counts, top_n=10):
    return division_counts.head(top_n)


def generate_division_rankings(division_counts):
    rankings = division_counts.reset_index()
    rankings.columns = ["division", "crime_count"]

    rankings.insert(0, "rank", range(1, len(rankings) + 1))

    return rankings


def create_division_visualization(division_rankings):
    fig, ax = plt.subplots()

    ax.bar(
        division_rankings["division"],
        division_rankings["crime_count"]
    )

    ax.set_title("Top Police Divisions by Crime Count")
    ax.set_xlabel("Police Division")
    ax.set_ylabel("Crime Count")
    ax.tick_params(axis="x", rotation=45)

    return fig