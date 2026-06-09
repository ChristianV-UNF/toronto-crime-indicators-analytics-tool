import pandas as pd
import matplotlib.pyplot as plt


def group_crimes_by_premises(df, premises_column="PREMISES_TYPE"):
    if premises_column not in df.columns:
        raise KeyError(f"{premises_column} column not found")

    premises_df = df[[premises_column]].copy()
    premises_df = premises_df.dropna()

    premises_df[premises_column] = (
        premises_df[premises_column]
        .astype(str)
        .replace("NSA", "Unknown")
    )

    return premises_df


def calculate_premises_frequencies(df, premises_column="PREMISES_TYPE"):
    premises_df = group_crimes_by_premises(df, premises_column)

    premises_frequencies = (
        premises_df[premises_column]
        .value_counts()
        .sort_values(ascending=False)
    )

    return premises_frequencies


def identify_top_premises_categories(premises_frequencies, top_n=10):
    """
    Return the top premises categories with the highest crime counts.
    """
    if top_n <= 0:
        raise ValueError("top_n must be greater than 0.")

    return premises_frequencies.head(top_n)


def generate_premises_rankings(premises_frequencies):
    rankings = premises_frequencies.reset_index()
    rankings.columns = ["premises_type", "crime_count"]

    rankings["premises_type"] = rankings["premises_type"].astype(str)

    rankings.insert(0, "rank", range(1, len(rankings) + 1))

    return rankings


def create_premises_visualization(premises_rankings):
    premises_rankings = premises_rankings.copy()
    premises_rankings["premises_type"] = (
        premises_rankings["premises_type"]
        .astype(str)
    )

    fig, ax = plt.subplots()

    ax.bar(
        premises_rankings["premises_type"],
        premises_rankings["crime_count"]
    )

    ax.set_title("Top Premises Types by Crime Count")
    ax.set_xlabel("Premises Type")
    ax.set_ylabel("Crime Count")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()

    return fig


def get_premises_type_summary(df, top_n=10):
    premises_frequencies = calculate_premises_frequencies(df)

    if premises_frequencies.empty:
        return {
            "top_premises_type": "No valid premises data",
            "crime_count": 0,
            "percentage": 0,
        }

    top_premises = identify_top_premises_categories(
        premises_frequencies,
        top_n=1
    )

    top_category = str(top_premises.index[0])
    top_count = int(top_premises.iloc[0])

    total_crimes = int(premises_frequencies.sum())
    percentage = round((top_count / total_crimes) * 100, 2) if total_crimes else 0

    return {
        "top_premises_type": top_category,
        "crime_count": top_count,
        "percentage": percentage,
    }


def get_premises_distribution_insight(df):
    summary = get_premises_type_summary(df)

    return {
        "insight": (
            f"The most frequent premises type is {summary['top_premises_type']} "
            f"with {summary['crime_count']} reported crimes, "
            f"representing {summary['percentage']}% of all incidents."
        )
    }