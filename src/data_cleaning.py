import pandas as pd


def identify_invalid_coordinates(df):
    invalid_coordinates = df[
        df["LAT_WGS84"].isna()
        | df["LONG_WGS84"].isna()
        | (df["LAT_WGS84"] == 0)
        | (df["LONG_WGS84"] == 0)
    ]

    return invalid_coordinates
def handle_placeholder_neighbourhoods(df):
    cleaned_df = df.copy()

    neighbourhood_columns = [
        "NEIGHBOURHOOD_158",
        "NEIGHBOURHOOD_140"
    ]

    for column in neighbourhood_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].replace("NSA", "Unknown")

    return cleaned_df
def process_missing_values(df):
    cleaned_df = df.copy()

    # Fill missing occurrence date details with unknown values
    occurrence_columns = [
        "OCC_YEAR",
        "OCC_MONTH",
        "OCC_DAY",
        "OCC_DOY",
        "OCC_DOW"
    ]

    for column in occurrence_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    # Fill missing location-related categories
    location_columns = [
        "LOCATION_TYPE",
        "PREMISES_TYPE"
    ]

    for column in location_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    return cleaned_df
def generate_cleaning_summary(df):
    summary = {
        "total_records": len(df),
        "invalid_coordinate_records": len(
            identify_invalid_coordinates(df)
        ),
        "missing_values": int(df.isnull().sum().sum())
    }

    return summary