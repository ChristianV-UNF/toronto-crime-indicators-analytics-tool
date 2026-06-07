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
    get_top_division_summary,
    get_division_activity_insight,
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
    assert result.loc["Unknown"] == 1


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

def test_invalid_top_n_raises_error(sample_division_df):
    counts = calculate_division_crime_counts(sample_division_df)
    with pytest.raises(ValueError, match="top_n must be greater than 0"):
        identify_top_divisions(counts, top_n=0)

def test_get_top_division_summary(sample_division_df):
    summary = get_top_division_summary(sample_division_df)

    assert summary["top_division"] == "D31"
    assert summary["crime_count"] == 3
    assert summary["percentage"] == 50.0


def test_get_division_activity_insight(sample_division_df):
    result = get_division_activity_insight(sample_division_df)

    assert "insight" in result
    assert "D31" in result["insight"]

def test_group_crimes_by_division_replaces_nsa():
    df = pd.DataFrame({"DIVISION": ["D14", "NSA", "NSA"]})
    result = group_crimes_by_division(df)
    assert "NSA" not in result["DIVISION"].values
    assert result["DIVISION"].tolist().count("Unknown") == 2