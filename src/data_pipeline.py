import pandas as pd

from src.data_loader import load_dataset
from src.data_cleaning import clean_invalid_records
from src.data_validation import generate_validation_report


def remove_invalid_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    coordinate_columns = ["LAT_WGS84", "LONG_WGS84"]

    if not all(column in df.columns for column in coordinate_columns):
        return df

    cleaned_df = df.copy()

    cleaned_df["LAT_WGS84"] = pd.to_numeric(
        cleaned_df["LAT_WGS84"],
        errors="coerce"
    )
    cleaned_df["LONG_WGS84"] = pd.to_numeric(
        cleaned_df["LONG_WGS84"],
        errors="coerce"
    )

    cleaned_df = cleaned_df.dropna(
        subset=["LAT_WGS84", "LONG_WGS84"]
    )

    cleaned_df = cleaned_df[
        cleaned_df["LAT_WGS84"].between(-90, 90)
        & cleaned_df["LONG_WGS84"].between(-180, 180)
    ]

    return cleaned_df


def load_clean_validate_dataset(file_path: str) -> dict:
    raw_df = load_dataset(file_path)

    cleaned_df = clean_invalid_records(raw_df)
    cleaned_df = remove_invalid_coordinates(cleaned_df)

    validation_report = generate_validation_report(cleaned_df)

    return {
        "raw_df": raw_df,
        "cleaned_df": cleaned_df,
        "validation_report": validation_report,
    }


def get_clean_dataset(file_path: str) -> pd.DataFrame:
    pipeline_result = load_clean_validate_dataset(file_path)

    return pipeline_result["cleaned_df"]