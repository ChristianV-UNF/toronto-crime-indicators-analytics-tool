import pandas as pd


def group_crimes_by_neighbourhood(
    df,
    neighbourhood_column="NEIGHBOURHOOD_158"
):
    if neighbourhood_column not in df.columns:
        raise KeyError(f"{neighbourhood_column} column not found")

    neighbourhood_df = df[[neighbourhood_column]].copy()
    neighbourhood_df = neighbourhood_df.dropna()

    neighbourhood_counts = (
        neighbourhood_df[neighbourhood_column]
        .value_counts()
        .sort_values(ascending=False)
    )

    return neighbourhood_counts