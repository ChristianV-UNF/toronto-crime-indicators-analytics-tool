import pandas as pd

from src.data_validation import generate_validation_report


def test_missing_values_are_reported():
    df = pd.DataFrame({
        "OFFENCE": ["Assault", None, "Robbery"],
        "OCC_DATE": ["2023-01-01", "2023-01-02", "2023-01-03"]
    })

    report = generate_validation_report(df)

    assert report["missing_values"]["OFFENCE"] == 1


def test_duplicate_records_are_identified():
    df = pd.DataFrame({
        "OFFENCE": ["Assault", "Assault"],
        "OCC_DATE": ["2023-01-01", "2023-01-01"]
    })

    report = generate_validation_report(df)

    assert report["duplicate_records"] == 1


def test_invalid_date_formats_are_detected():
    df = pd.DataFrame({
        "OFFENCE": ["Assault", "Robbery"],
        "OCC_DATE": ["2023-01-01", "not-a-date"]
    })

    report = generate_validation_report(df)

    assert report["invalid_date_formats"]["OCC_DATE"] == 1


def test_validation_report_is_generated():
    df = pd.DataFrame({
        "OFFENCE": ["Assault"],
        "OCC_DATE": ["2023-01-01"]
    })

    report = generate_validation_report(df)

    assert isinstance(report, dict)