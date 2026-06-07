import pandas as pd
import pytest
from matplotlib.figure import Figure

from src.premises_analysis import (
    group_crimes_by_premises,
    calculate_premises_frequencies,
    identify_top_premises_categories,
    generate_premises_rankings,
    create_premises_visualization,
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
    assert result.loc["NSA"] == 1


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