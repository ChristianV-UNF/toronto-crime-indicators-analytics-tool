# tests/test_police_division_analysis.py
import pandas as pd
import pytest
from matplotlib.figure import Figure

from src.police_division_analysis import (
    group_crimes_by_division,
    calculate_division_crime_counts,
    identify_top_divisions,
    generate_division_rankings,
    create_division_visualization,
)

@pytest.fixture
def sample_division_df():
    return pd.DataFrame({
        "DIVISION": ["D14", "D14", "D31", "D31", "D31", "NSA"]
    })

def test_group_crimes_by_division(sample_division_df):
    result = group_crimes_by_division(sample_division_df)

    assert list(result.columns) == ["DIVISION"]
    assert len(result) == 6


def test_group_crimes_by_division_missing_column():
    df = pd.DataFrame({"OTHER": ["A", "B"]})

    with pytest.raises(KeyError, match="DIVISION"):
        group_crimes_by_division(df)


def test_calculate_division_crime_counts(sample_division_df):
    result = calculate_division_crime_counts(sample_division_df)

    assert result.loc["D31"] == 3
    assert result.loc["D14"] == 2
    assert result.loc["NSA"] == 1


def test_identify_top_divisions(sample_division_df):
    counts = calculate_division_crime_counts(sample_division_df)
    result = identify_top_divisions(counts, top_n=2)

    assert len(result) == 2
    assert result.index[0] == "D31"


def test_generate_division_rankings(sample_division_df):
    counts = calculate_division_crime_counts(sample_division_df)
    top = identify_top_divisions(counts, top_n=3)
    result = generate_division_rankings(top)

    assert list(result.columns) == ["rank", "division", "crime_count"]
    assert result.iloc[0]["rank"] == 1
    assert result.iloc[0]["division"] == "D31"


def test_create_division_visualization(sample_division_df):
    counts = calculate_division_crime_counts(sample_division_df)
    rankings = generate_division_rankings(counts)
    fig = create_division_visualization(rankings)

    assert isinstance(fig, Figure)