import pandas as pd
from data_cleaning import (
    identify_invalid_coordinates,
    handle_placeholder_neighbourhoods,
    process_missing_values,
    generate_cleaning_summary
)

df = pd.read_csv("data/Toronto_Crime_Indicators.csv")

invalid_records = identify_invalid_coordinates(df)
print("Invalid coordinate records found:", len(invalid_records))

neighbourhood_cleaned_df = handle_placeholder_neighbourhoods(df)
nsa_remaining = (
    (neighbourhood_cleaned_df["NEIGHBOURHOOD_158"] == "NSA").sum()
    +
    (neighbourhood_cleaned_df["NEIGHBOURHOOD_140"] == "NSA").sum()
)
print("NSA values remaining:", nsa_remaining)

missing_cleaned_df = process_missing_values(df)
missing_remaining = missing_cleaned_df.isnull().sum().sum()
print("Missing values remaining:", missing_remaining)

summary = generate_cleaning_summary(df)
print("Cleaning Summary Report:", summary)