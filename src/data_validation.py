import pandas as pd


def generate_validation_report(df):
    report = {}

    # Missing values
    report["missing_values"] = df.isnull().sum().to_dict()

    # Duplicate records
    report["duplicate_records"] = int(df.duplicated().sum())

    # Invalid date formats
    invalid_dates = {}

    if "OCC_DATE" in df.columns:
        parsed_dates = pd.to_datetime(df["OCC_DATE"], errors="coerce")
        invalid_dates["OCC_DATE"] = int(parsed_dates.isna().sum())

    report["invalid_date_formats"] = invalid_dates

    return report