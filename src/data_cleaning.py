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

    for column in ["NEIGHBOURHOOD_158", "NEIGHBOURHOOD_140"]:
        if column in cleaned_df.columns:
            cleaned_df[column] = cleaned_df[column].replace("NSA", "Unknown")

    return cleaned_df

# Updated missing value handling below to use pandas dtype-safe checks instead of strict "object" dtype comparison.
# The previous implementation failed when some non-numeric columns (e.g., strings or categories like 'OFFENCE')
# were inferred as non-object dtypes, causing them to be filled with 0 instead of "Unknown".
# This change ensures all non-numeric columns consistently receive "Unknown", while numeric columns are filled with 0.

def process_missing_values(df):
    cleaned_df = df.copy()

    for column in cleaned_df.columns:
        if pd.api.types.is_numeric_dtype(cleaned_df[column]):
            cleaned_df[column] = cleaned_df[column].fillna(0)
        else:
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    return cleaned_df

"""
def process_missing_values(df):
    cleaned_df = df.copy()

    for column in cleaned_df.columns:
        if cleaned_df[column].dtype == "object":
            cleaned_df[column] = cleaned_df[column].fillna("Unknown")
        else:
            cleaned_df[column] = cleaned_df[column].fillna(0)

    return cleaned_df
"""

def clean_invalid_records(df):
    cleaned_df = handle_placeholder_neighbourhoods(df)
    cleaned_df = process_missing_values(cleaned_df)

    return cleaned_df


def generate_cleaning_summary(df):
    cleaned_df = clean_invalid_records(df)

    summary = {
        "total_records": len(df),
        "invalid_coordinate_records": len(identify_invalid_coordinates(df)),
        "missing_values_before_cleaning": int(df.isnull().sum().sum()),
        "missing_values_after_cleaning": int(cleaned_df.isnull().sum().sum()),
        "nsa_values_before_cleaning": int(
            ((df["NEIGHBOURHOOD_158"] == "NSA").sum() if "NEIGHBOURHOOD_158" in df.columns else 0)
            + ((df["NEIGHBOURHOOD_140"] == "NSA").sum() if "NEIGHBOURHOOD_140" in df.columns else 0)
        ),
        "nsa_values_after_cleaning": int(
            ((cleaned_df["NEIGHBOURHOOD_158"] == "NSA").sum() if "NEIGHBOURHOOD_158" in cleaned_df.columns else 0)
            + ((cleaned_df["NEIGHBOURHOOD_140"] == "NSA").sum() if "NEIGHBOURHOOD_140" in cleaned_df.columns else 0)
        ),
        "cleaned_records": len(cleaned_df),
    }

    return summary