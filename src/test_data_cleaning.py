import pandas as pd
from src.data_cleaning import identify_invalid_coordinates

df = pd.read_csv("data/Toronto_Crime_Indicators.csv")

invalid_records = identify_invalid_coordinates(df)

print("Invalid coordinate records found:", len(invalid_records))
print(invalid_records.head())