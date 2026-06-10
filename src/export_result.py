import pandas as pd

from src.hourly_analysis import generate_hourly_summary_table
from src.neighbourhood_analysis import (
    calculate_crime_counts,
    generate_neighbourhood_rankings,
    identify_top_crime_neighbourhoods,
)
from src.offence_analysis import prepare_offence_visualization_data
from src.police_division_analysis import (
    calculate_division_crime_counts,
    identify_top_divisions,
    generate_division_rankings,
)
from src.premises_analysis import (
    calculate_premises_frequencies,
    identify_top_premises_categories,
    generate_premises_rankings,
)


EXPORT_OPTIONS = {
    "filtered_records": "Filtered Crime Records",
    "hourly_summary": "Hourly Crime Summary",
    "neighbourhood_rankings": "Neighbourhood Rankings",
    "offence_distribution": "Offence Distribution",
    "division_rankings": "Police Division Rankings",
    "premises_rankings": "Premises Type Rankings",
}


def validate_export_dataframe(df):
    if df is None or df.empty:
        raise ValueError("No data available for export.")


def prepare_export_data(df, export_type="filtered_records"):
    validate_export_dataframe(df)

    if export_type == "filtered_records":
        return df.copy()

    if export_type == "hourly_summary":
        return generate_hourly_summary_table(df)

    if export_type == "neighbourhood_rankings":
        counts = calculate_crime_counts(df)
        top = identify_top_crime_neighbourhoods(counts)
        return generate_neighbourhood_rankings(top)

    if export_type == "offence_distribution":
        return prepare_offence_visualization_data(df, top_n=10)

    if export_type == "division_rankings":
        counts = calculate_division_crime_counts(df)
        top = identify_top_divisions(counts, top_n=10)
        return generate_division_rankings(top)

    if export_type == "premises_rankings":
        frequencies = calculate_premises_frequencies(df)
        top = identify_top_premises_categories(frequencies, top_n=10)
        return generate_premises_rankings(top)

    raise ValueError(f"Unsupported export type: {export_type}")


def convert_dataframe_to_csv(df):
    return df.to_csv(index=False)


def generate_export_filename(export_type):
    return f"toronto_crime_{export_type}.csv"


def get_export_confirmation_message(filename, row_count):
    return (
        f"Export ready: {filename} contains {row_count:,} records."
    )