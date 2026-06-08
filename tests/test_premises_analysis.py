import pandas as pd
import pytest
from matplotlib.figure import Figure

from src.premises_analysis import (
    group_crimes_by_premises,
    calculate_premises_frequencies,
    identify_top_premises_categories,
    generate_premises_rankings,
    create_premises_visualization,
    get_premises_type_summary,
    get_premises_distribution_insight,
)


@pytest.fixture
def sample_premises_df():
    return pd.DataFrame({
        "PREMISES_TYPE": [
            "Outside",
            "Outside",
            "House",
            "House",
            "House",
            "NSA",
        ]
    })


def test_group_crimes_by_premises(sample_premises_df):
    result = group_crimes_by_premises(sample_premises_df)

    assert list(result.columns) == ["PREMISES_TYPE"]
    assert len(result) == 6


def test_group_crimes_by_premises_missing_column():
    df = pd.DataFrame({"OTHER": ["A", "B"]})

    with pytest.raises(KeyError, match="PREMISES_TYPE"):
        group_crimes_by_premises(df)


def test_calculate_premises_frequencies(sample_premises_df):
    result = calculate_premises_frequencies(sample_premises_df)

    assert result.loc["House"] == 3
    assert result.loc["Outside"] == 2
    assert result.loc["Unknown"] == 1 


def test_identify_top_premises_categories(sample_premises_df):
    frequencies = calculate_premises_frequencies(sample_premises_df)
    result = identify_top_premises_categories(frequencies, top_n=2)

    assert len(result) == 2
    assert result.index[0] == "House"


def test_generate_premises_rankings(sample_premises_df):
    frequencies = calculate_premises_frequencies(sample_premises_df)
    top = identify_top_premises_categories(frequencies, top_n=3)
    result = generate_premises_rankings(top)

    assert list(result.columns) == ["rank", "premises_type", "crime_count"]
    assert result.iloc[0]["rank"] == 1
    assert result.iloc[0]["premises_type"] == "House"


def test_create_premises_visualization(sample_premises_df):
    frequencies = calculate_premises_frequencies(sample_premises_df)
    rankings = generate_premises_rankings(frequencies)
    fig = create_premises_visualization(rankings)

    assert isinstance(fig, Figure)

def test_invalid_top_n_raises_error(sample_premises_df):
    frequencies = calculate_premises_frequencies(sample_premises_df)

    with pytest.raises(ValueError, match="top_n must be greater than 0"):
        identify_top_premises_categories(frequencies, top_n=0)


def test_group_crimes_by_premises_replaces_nsa():
    df = pd.DataFrame({"PREMISES_TYPE": ["House", "NSA", "NSA"]})
    result = group_crimes_by_premises(df)

    assert "NSA" not in result["PREMISES_TYPE"].values
    assert result["PREMISES_TYPE"].tolist().count("Unknown") == 2


def test_get_premises_type_summary(sample_premises_df):
    summary = get_premises_type_summary(sample_premises_df)

    assert summary["top_premises_type"] == "House"
    assert summary["crime_count"] == 3
    assert summary["percentage"] == 50.0


def test_get_premises_distribution_insight(sample_premises_df):
    result = get_premises_distribution_insight(sample_premises_df)

    assert "insight" in result
    assert "House" in result["insight"]