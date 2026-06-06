from pathlib import Path

import pandas as pd
import pytest

from src.offence_analysis import (
    analyze_offence_distribution,
    get_most_frequent_offences,
    get_top_offence_summary,
    get_offence_distribution_insight,
    prepare_offence_visualization_data,
)


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Toronto_Crime_Indicators.csv"


def load_data():
    return pd.read_csv(CSV_PATH)


def test_csv_file_exists():
    assert CSV_PATH.exists()


def test_analyze_offence_distribution_returns_expected_columns():
    df = load_data()

    result = analyze_offence_distribution(df)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["OFFENCE", "crime_count", "percentage"]


def test_crimes_are_grouped_by_offence_type():
    df = load_data()

    result = analyze_offence_distribution(df)

    assert len(result) == df["OFFENCE"].fillna("Unknown").nunique()


def test_percentages_are_calculated():
    df = load_data()

    result = analyze_offence_distribution(df)

    assert round(result["percentage"].sum()) == 100


def test_most_frequent_offences_identified():
    df = load_data()

    result = get_most_frequent_offences(df, top_n=10)

    assert len(result) <= 10
    assert result["crime_count"].is_monotonic_decreasing


def test_top_offence_summary_returns_dictionary():
    df = load_data()

    summary = get_top_offence_summary(df)

    assert isinstance(summary, dict)
    assert "most_frequent_offence" in summary
    assert "crime_count" in summary
    assert "percentage" in summary


def test_prepare_offence_visualization_data():
    df = load_data()

    chart_data = prepare_offence_visualization_data(df, top_n=10)

    assert isinstance(chart_data, pd.DataFrame)
    assert list(chart_data.columns) == ["OFFENCE", "crime_count", "percentage"]
    assert len(chart_data) <= 10

def test_offence_distribution_insight():
    df = load_data()

    insight = get_offence_distribution_insight(df)

    assert isinstance(insight, dict)
    assert "insight" in insight
    assert len(insight["insight"]) > 0


def test_missing_offence_column_raises_error():
    df = pd.DataFrame({"OTHER_COLUMN": ["A", "B", "C"]})

    with pytest.raises(ValueError, match="OFFENCE column is missing"):
        analyze_offence_distribution(df)


def test_empty_dataset_raises_error():
    df = pd.DataFrame(columns=["OFFENCE"])

    with pytest.raises(ValueError, match="Dataset is empty"):
        analyze_offence_distribution(df)


def test_invalid_top_n_raises_error():
    df = load_data()

    with pytest.raises(ValueError, match="top_n must be greater than 0"):
        get_most_frequent_offences(df, top_n=0)