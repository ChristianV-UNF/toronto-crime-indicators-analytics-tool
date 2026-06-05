import pandas as pd

from src.data_validation import generate_validation_report, detect_invalid_dates


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


def test_missing_dates_are_not_counted_as_invalid_formats():
    df = pd.DataFrame({
        "OFFENCE": ["Assault", "Robbery", "Theft"],
        "OCC_DATE": ["2023-01-01", None, "not-a-date"]
    })

    report = generate_validation_report(df)

    assert report["missing_values"]["OCC_DATE"] == 1
    assert report["invalid_date_formats"]["OCC_DATE"] == 1


def test_multiple_date_columns_are_validated():
    df = pd.DataFrame({
        "OCC_DATE": ["2023-01-01", "bad-date"],
        "REPORT_DATE": ["2023-02-01", "wrong-date"],
        "OFFENCE": ["Assault", "Robbery"]
    })

    report = generate_validation_report(df)

    assert report["invalid_date_formats"]["OCC_DATE"] == 1
    assert report["invalid_date_formats"]["REPORT_DATE"] == 1


def test_detect_invalid_dates_accepts_custom_date_columns():
    df = pd.DataFrame({
        "START_DATE": ["2023-01-01", "invalid-date"],
        "END_DATE": ["2023-02-01", None]
    })

    result = detect_invalid_dates(df, date_columns=["START_DATE", "END_DATE"])

    assert result["START_DATE"] == 1
    assert result["END_DATE"] == 0


def test_validation_report_is_generated():
    df = pd.DataFrame({
        "OFFENCE": ["Assault"],
        "OCC_DATE": ["2023-01-01"]
    })

    report = generate_validation_report(df)

    assert isinstance(report, dict)