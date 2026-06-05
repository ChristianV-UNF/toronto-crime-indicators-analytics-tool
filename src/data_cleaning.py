import pandas as pd


def identify_invalid_coordinates(df):
    invalid_coordinates = df[
        df["LAT_WGS84"].isna()
        | df["LONG_WGS84"].isna()
        | (df["LAT_WGS84"] == 0)
        | (df["LONG_WGS84"] == 0)
    ]

    return invalid_coordinates