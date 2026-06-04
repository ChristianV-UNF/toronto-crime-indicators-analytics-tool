import pandas as pd


def count_missing_values(df):
    return df.isnull().sum().to_dict()


def count_duplicate_records(df):
    return int(df.duplicated().sum())


def detect_invalid_dates(df, date_column="OCC_DATE"):
    invalid_dates = {}

    if date_column in df.columns:
        parsed_dates = pd.to_datetime(
            df[date_column],
            errors="coerce"
        )

        invalid_dates[date_column] = int(
            parsed_dates.isna().sum()
        )

    return invalid_dates


def generate_validation_report(df):
    return {
        "missing_values": count_missing_values(df),
        "duplicate_records": count_duplicate_records(df),
        "invalid_date_formats": detect_invalid_dates(df)
    }