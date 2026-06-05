import pandas as pd


def count_missing_values(df):
    return df.isnull().sum().to_dict()


def count_duplicate_records(df):
    return int(df.duplicated().sum())


def detect_invalid_dates(df, date_columns=None):
    invalid_dates = {}

    if date_columns is None:
        date_columns = [
            column for column in df.columns
            if "DATE" in column.upper()
        ]

    for column in date_columns:
        if column in df.columns:
            non_missing_dates = df[column].dropna()

            parsed_dates = pd.to_datetime(
                non_missing_dates,
                errors="coerce"
            )

            invalid_dates[column] = int(parsed_dates.isna().sum())

    return invalid_dates


def generate_validation_report(df):
    return {
        "missing_values": count_missing_values(df),
        "duplicate_records": count_duplicate_records(df),
        "invalid_date_formats": detect_invalid_dates(df)
    }