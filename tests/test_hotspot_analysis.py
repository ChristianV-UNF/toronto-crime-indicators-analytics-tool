import pandas as pd
import pytest

from src.hotspot_analysis import (
    process_geographic_coordinates,
    identify_crime_hotspots,
    highlight_high_density_locations
)


def test_process_geographic_coordinates():
    df = pd.DataFrame({
        "LAT_WGS84": [43.6, None, 0],
        "LONG_WGS84": [-79.3, -79.4, 0]
    })

    result = process_geographic_coordinates(df)

    assert len(result) == 1


def test_identify_crime_hotspots():
    df = pd.DataFrame({
        "LAT_WGS84": [43.6, 43.6, 43.7],
        "LONG_WGS84": [-79.3, -79.3, -79.4]
    })

    hotspots = identify_crime_hotspots(df)

    assert hotspots.iloc[0]["crime_count"] == 2


def test_high_density_locations():
    hotspots = pd.DataFrame({
        "LAT_WGS84": [43.6, 43.7],
        "LONG_WGS84": [-79.3, -79.4],
        "crime_count": [1500, 500]
    })

    result = highlight_high_density_locations(
        hotspots,
        threshold=1000
    )

    assert len(result) == 1


def test_missing_coordinate_columns():
    df = pd.DataFrame({
        "LAT": [43.6]
    })

    with pytest.raises(KeyError):
        process_geographic_coordinates(df)