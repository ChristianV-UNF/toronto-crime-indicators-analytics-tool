import pandas as pd
from matplotlib.figure import Figure

from src.hourly_analysis import (
    extract_hour_data,
    group_crimes_by_hour,
    generate_hourly_summary_table,
    create_hourly_crime_visualization,
    identify_peak_hours,
)


def test_extract_hour_data():
    df = pd.DataFrame({
        "OCC_HOUR": [1, 5, 12]
    })

    result = extract_hour_data(df)

    assert list(result["OCC_HOUR"]) == [1, 5, 12]


def test_extract_hour_data_excludes_invalid_hours():
    df = pd.DataFrame({
        "OCC_HOUR": [0, 1, 23, -1, 24, 99, "bad", None]
    })

    result = extract_hour_data(df)

    assert list(result["OCC_HOUR"]) == [0, 1, 23]


def test_group_crimes_by_hour():
    df = pd.DataFrame({
        "OCC_HOUR": [1, 1, 2, 2, 2]
    })

    result = group_crimes_by_hour(df)

    assert result.loc[1] == 2
    assert result.loc[2] == 3


def test_generate_hourly_summary_table():
    df = pd.DataFrame({
        "OCC_HOUR": [1, 1, 2, 2, 2]
    })

    result = generate_hourly_summary_table(df)

    assert list(result.columns) == ["hour", "crime_count"]
    assert result.loc[result["hour"] == 1, "crime_count"].iloc[0] == 2
    assert result.loc[result["hour"] == 2, "crime_count"].iloc[0] == 3


def test_create_hourly_crime_visualization():
    hourly_summary = pd.DataFrame({
        "hour": [1, 2, 3],
        "crime_count": [10, 25, 15]
    })

    fig = create_hourly_crime_visualization(hourly_summary)

    assert isinstance(fig, Figure)


def test_identify_peak_hours():
    hourly_counts = pd.Series({
        1: 10,
        2: 25,
        3: 15
    })

    result = identify_peak_hours(hourly_counts)

    assert result == [2]