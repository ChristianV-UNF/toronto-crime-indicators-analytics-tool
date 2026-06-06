import pandas as pd


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