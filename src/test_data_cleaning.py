from pathlib import Path

import pandas as pd

from src.data_cleaning import (
    identify_invalid_coordinates,
    handle_placeholder_neighbourhoods,
    process_missing_values,
    generate_cleaning_summary,
    clean_invalid_records,
)


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Toronto_Crime_Indicators.csv"


def load_data():
    return pd.read_csv(CSV_PATH)


def test_csv_file_exists():
    assert CSV_PATH.exists()


def test_identify_invalid_coordinates():
    df = load_data()

    invalid_records = identify_invalid_coordinates(df)

    assert isinstance(invalid_records, pd.DataFrame)


def test_handle_placeholder_neighbourhoods():
    df = load_data()

    cleaned_df = handle_placeholder_neighbourhoods(df)

    if "NEIGHBOURHOOD_158" in cleaned_df.columns:
        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_158"].values

    if "NEIGHBOURHOOD_140" in cleaned_df.columns:
        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_140"].values


def test_process_missing_values():
    df = load_data()

    cleaned_df = process_missing_values(df)

    assert cleaned_df.isnull().sum().sum() == 0


def test_generate_cleaning_summary():
    df = load_data()

    summary = generate_cleaning_summary(df)

    assert isinstance(summary, dict)
    assert summary["total_records"] == len(df)
    assert "invalid_coordinate_records" in summary
    assert "missing_values_before_cleaning" in summary
    assert "missing_values_after_cleaning" in summary
    assert "nsa_values_before_cleaning" in summary
    assert "nsa_values_after_cleaning" in summary
    assert "cleaned_records" in summary


def test_clean_invalid_records():
    df = load_data()

    cleaned_df = clean_invalid_records(df)

    assert isinstance(cleaned_df, pd.DataFrame)
    assert cleaned_df.isnull().sum().sum() == 0