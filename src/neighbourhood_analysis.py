import pandas as pd
import matplotlib.pyplot as plt


def group_crimes_by_neighbourhood(
    df,
    neighbourhood_column="NEIGHBOURHOOD_158"
):
    if neighbourhood_column not in df.columns:
        raise KeyError(f"{neighbourhood_column} column not found")

    neighbourhood_df = df[[neighbourhood_column]].copy()
    neighbourhood_df = neighbourhood_df.dropna()

    return neighbourhood_df


def calculate_crime_counts(
    df,
    neighbourhood_column="NEIGHBOURHOOD_158"
):
    neighbourhood_df = group_crimes_by_neighbourhood(
        df,
        neighbourhood_column
    )

    neighbourhood_counts = (
        neighbourhood_df[neighbourhood_column]
        .value_counts()
        .sort_values(ascending=False)
    )

    return neighbourhood_counts

def identify_top_crime_neighbourhoods(
    neighbourhood_counts,
    top_n=10
):
    """
    Return the top neighbourhoods with the highest crime counts.
    """

    return neighbourhood_counts.head(top_n)

def generate_neighbourhood_rankings(
    neighbourhood_counts
):
    rankings = neighbourhood_counts.reset_index()
    rankings.columns = ["neighbourhood", "crime_count"]

    rankings.insert(
        0,
        "rank",
        range(1, len(rankings) + 1)
    )

    return rankings


def create_neighbourhood_visualization(neighbourhood_rankings):
    fig, ax = plt.subplots()

    ax.bar(
        neighbourhood_rankings["neighbourhood"],
        neighbourhood_rankings["crime_count"]
    )

    ax.set_title("Top Crime Neighbourhoods")
    ax.set_xlabel("Neighbourhood")
    ax.set_ylabel("Crime Count")

    ax.tick_params(axis="x", rotation=45)

    return fig