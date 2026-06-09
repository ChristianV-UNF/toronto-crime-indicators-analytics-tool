import pandas as pd
import plotly.express as px

def process_geographic_coordinates(
    df,
    latitude_column="LAT_WGS84",
    longitude_column="LONG_WGS84"
):
    if latitude_column not in df.columns:
        raise KeyError(f"{latitude_column} column not found")

    if longitude_column not in df.columns:
        raise KeyError(f"{longitude_column} column not found")

    coordinates_df = df[
        [latitude_column, longitude_column]
    ].copy()

    coordinates_df[latitude_column] = pd.to_numeric(
        coordinates_df[latitude_column],
        errors="coerce"
    )

    coordinates_df[longitude_column] = pd.to_numeric(
        coordinates_df[longitude_column],
        errors="coerce"
    )

    coordinates_df = coordinates_df.dropna()

    coordinates_df = coordinates_df[
        (coordinates_df[latitude_column] != 0)
        & (coordinates_df[longitude_column] != 0)
    ]

    return coordinates_df

def identify_crime_hotspots(
    coordinates_df,
    latitude_column="LAT_WGS84",
    longitude_column="LONG_WGS84"
):
    hotspot_counts = (
        coordinates_df
        .groupby(
            [latitude_column, longitude_column]
        )
        .size()
        .reset_index(name="crime_count")
        .sort_values(
            by="crime_count",
            ascending=False
        )
    )

    return hotspot_counts

def highlight_high_density_locations(
    hotspots,
    threshold=1000
):
    return hotspots[
        hotspots["crime_count"] >= threshold
    ]

def create_hotspot_map_visualization(
    hotspots,
    latitude_column="LAT_WGS84",
    longitude_column="LONG_WGS84"
):
    fig = px.scatter_mapbox(
        hotspots,
        lat=latitude_column,
        lon=longitude_column,
        size="crime_count",
        color="crime_count",
        hover_data=["crime_count"],
        zoom=10,
        height=600,
        title="Toronto Crime Hotspot Map"
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={
            "r": 0,
            "t": 40,
            "l": 0,
            "b": 0
        }
    )

    return fig