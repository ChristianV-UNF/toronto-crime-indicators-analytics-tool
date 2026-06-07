import pandas as pd
import matplotlib.pyplot as plt


def group_crimes_by_division(df, division_column="DIVISION"):
    if division_column not in df.columns:
        raise KeyError(f"{division_column} column not found")

    division_df = df[[division_column]].copy()
    division_df = division_df.dropna()
    division_df[division_column] = division_df[division_column].replace("NSA", "Unknown")

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
    """
    Return the top police divisions with the highest crime counts.
    """
    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")
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

def get_top_division_summary(df, top_n=10):
    division_counts = calculate_division_crime_counts(df)
    top_divisions = identify_top_divisions(division_counts, top_n=1)
    top_division = top_divisions.index[0]
    top_count = int(top_divisions.iloc[0])

    total_crimes = int(division_counts.sum())
    percentage = round((top_count / total_crimes) * 100, 2) if total_crimes else 0

    return {
        "top_division": top_division,
        "crime_count": top_count,
        "percentage": percentage,
    }


def get_division_activity_insight(df):
    summary = get_top_division_summary(df)

    return {
        "insight": (
            f"The police division with the most reported crimes is "
            f"{summary['top_division']} with {summary['crime_count']} cases, "
            f"representing {summary['percentage']}% of all division records."
        )
    }