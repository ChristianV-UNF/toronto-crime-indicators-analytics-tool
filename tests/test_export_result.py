import pandas as pd
import pytest

from src.export_result import (
    EXPORT_OPTIONS,
    validate_export_dataframe,
    prepare_export_data,
    convert_dataframe_to_csv,
    generate_export_filename,
    get_export_confirmation_message,
)


def sample_data():
    return pd.DataFrame({
        "OCC_HOUR": [1, 2, 2],
        "NEIGHBOURHOOD_158": [
            "Downtown",
            "Scarborough",
            "Downtown"
        ],
        "OFFENCE": [
            "Assault",
            "Theft",
            "Theft"
        ],
        "DIVISION": [
            "D11",
            "D12",
            "D11"
        ],
        "PREMISES_TYPE": [
            "House",
            "Store",
            "House"
        ]
    })


def test_validate_export_dataframe_valid():
    df = sample_data()

    # Should not raise an exception
    validate_export_dataframe(df)


def test_validate_export_dataframe_none():
    with pytest.raises(ValueError):
        validate_export_dataframe(None)


def test_validate_export_dataframe_empty():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_export_dataframe(df)


def test_prepare_export_filtered_records():
    df = sample_data()

    result = prepare_export_data(
        df,
        export_type="filtered_records"
    )

    assert isinstance(result, pd.DataFrame)
    assert result.equals(df)


def test_prepare_export_invalid_type():
    df = sample_data()

    with pytest.raises(ValueError):
        prepare_export_data(
            df,
            export_type="invalid_export"
        )


def test_convert_dataframe_to_csv():
    df = pd.DataFrame({
        "A": [1, 2]
    })

    csv_data = convert_dataframe_to_csv(df)

    assert isinstance(csv_data, str)
    assert "A" in csv_data
    assert "1" in csv_data
    assert "2" in csv_data


def test_generate_export_filename():
    filename = generate_export_filename(
        "hourly_summary"
    )

    assert (
        filename
        == "toronto_crime_hourly_summary.csv"
    )


def test_export_confirmation_message():
    message = get_export_confirmation_message(
        "test.csv",
        1234
    )

    assert "test.csv" in message
    assert "1,234" in message
    assert "Export ready" in message


def test_export_options_exist():
    assert "filtered_records" in EXPORT_OPTIONS
    assert "hourly_summary" in EXPORT_OPTIONS
    assert "neighbourhood_rankings" in EXPORT_OPTIONS