import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.figure
import pytest

from src.neighbourhood_analysis import (
    group_crimes_by_neighbourhood,
    calculate_crime_counts,
    identify_top_crime_neighbourhoods,
    generate_neighbourhood_rankings,
    create_neighbourhood_visualization,
)


def sample_data():
    return pd.DataFrame({
        "NEIGHBOURHOOD_158": [
            "Downtown",
            "Scarborough",
            "Downtown",
            "North York",
            "Downtown",
            "Scarborough",
            None,
        ]
    })


def test_group_crimes_by_neighbourhood():
    df = sample_data()

    result = group_crimes_by_neighbourhood(df)

    assert "NEIGHBOURHOOD_158" in result.columns
    assert result["NEIGHBOURHOOD_158"].isna().sum() == 0
    assert len(result) == 6


def test_group_crimes_by_neighbourhood_missing_column():
    df = pd.DataFrame({
        "AREA": ["A", "B"]
    })

    with pytest.raises(KeyError):
        group_crimes_by_neighbourhood(df)


def test_calculate_crime_counts():
    df = sample_data()

    result = calculate_crime_counts(df)

    assert result["Downtown"] == 3
    assert result["Scarborough"] == 2
    assert result["North York"] == 1


def test_identify_top_crime_neighbourhoods():
    df = sample_data()

    counts = calculate_crime_counts(df)

    result = identify_top_crime_neighbourhoods(
        counts,
        top_n=2
    )

    assert len(result) == 2
    assert result.index[0] == "Downtown"
    assert result.iloc[0] == 3


def test_identify_top_crime_neighbourhoods_zero():
    df = sample_data()

    counts = calculate_crime_counts(df)

    result = identify_top_crime_neighbourhoods(
        counts,
        top_n=0
    )

    assert len(result) == 0


def test_generate_neighbourhood_rankings():
    df = sample_data()

    counts = calculate_crime_counts(df)

    rankings = generate_neighbourhood_rankings(counts)

    assert "rank" in rankings.columns
    assert "neighbourhood" in rankings.columns
    assert "crime_count" in rankings.columns

    assert rankings.iloc[0]["rank"] == 1
    assert rankings.iloc[0]["neighbourhood"] == "Downtown"
    assert rankings.iloc[0]["crime_count"] == 3


def test_create_neighbourhood_visualization():
    df = sample_data()

    counts = calculate_crime_counts(df)

    rankings = generate_neighbourhood_rankings(counts)

    fig = create_neighbourhood_visualization(rankings)

    assert isinstance(fig, matplotlib.figure.Figure)
