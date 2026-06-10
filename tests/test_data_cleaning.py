

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
    
def create_sample_dirty_data():
        return pd.DataFrame({
        "LAT_WGS84": [43.65, 0, None, 43.70],
        "LONG_WGS84": [-79.38, -79.40, -79.41, 0],
        "NEIGHBOURHOOD_158": ["Downtown", "NSA", None, "Scarborough"],
        "NEIGHBOURHOOD_140": ["NSA", "North York", "Etobicoke", None],
        "OFFENCE": ["Assault", None, "Theft", "Robbery"],
        "REPORT_YEAR": [2024, 2024, None, 2025],
    })


def test_identify_invalid_coordinates_with_sample_data():
        df = create_sample_dirty_data()

        invalid_records = identify_invalid_coordinates(df)

        assert len(invalid_records) == 3


def test_handle_placeholder_neighbourhoods_with_sample_data():
        df = create_sample_dirty_data()

        cleaned_df = handle_placeholder_neighbourhoods(df)

        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_158"].values
        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_140"].values


def test_process_missing_values_with_sample_data():
        df = create_sample_dirty_data()

        cleaned_df = process_missing_values(df)

        assert cleaned_df.isnull().sum().sum() == 0
        assert "Unknown" in cleaned_df["OFFENCE"].values
        assert 0 in cleaned_df["REPORT_YEAR"].values


def test_clean_invalid_records_with_sample_data():
        df = create_sample_dirty_data()

        cleaned_df = clean_invalid_records(df)

        assert cleaned_df.isnull().sum().sum() == 0
        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_158"].values
        assert "NSA" not in cleaned_df["NEIGHBOURHOOD_140"].values


def test_generate_cleaning_summary_with_sample_data():
        df = create_sample_dirty_data()

        summary = generate_cleaning_summary(df)

        assert summary["total_records"] == 4
        assert summary["invalid_coordinate_records"] == 3
        assert summary["missing_values_before_cleaning"] == 5
        assert summary["missing_values_after_cleaning"] == 0
        assert summary["nsa_values_before_cleaning"] == 2
        assert summary["nsa_values_after_cleaning"] == 0
        assert summary["cleaned_records"] == 4