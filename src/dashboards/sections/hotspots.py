import streamlit as st

from src.hotspot_analysis import (
    process_geographic_coordinates,
    identify_crime_hotspots,
    highlight_high_density_locations,
    create_hotspot_map_visualization,
)


def render_hotspots_section(filtered_df):
    st.header("Crime Hotspot Analysis")

    if filtered_df.empty:
        st.info("No records available for the current filter selection.")
        return

    coordinates_df = process_geographic_coordinates(filtered_df)
    st.write(f"Valid coordinate records: {len(coordinates_df):,}")

    if coordinates_df.empty:
        st.info("No valid coordinate records found for the current filter selection.")
        return

    st.dataframe(coordinates_df.head())

    hotspots = identify_crime_hotspots(coordinates_df)

    st.subheader("Top Crime Hotspots")
    st.dataframe(hotspots.head(10))

    high_density_locations = highlight_high_density_locations(hotspots)

    st.subheader("High-Density Crime Locations")
    st.dataframe(high_density_locations)

    st.subheader("Crime Hotspot Map")

    if high_density_locations.empty:
        st.info("No high-density crime locations found for the current filter selection.")
        return

    high_density_locations = high_density_locations.copy()
    high_density_locations["LAT_WGS84"] = high_density_locations["LAT_WGS84"].astype(float)
    high_density_locations["LONG_WGS84"] = high_density_locations["LONG_WGS84"].astype(float)
    high_density_locations["crime_count"] = high_density_locations["crime_count"].astype(int)

    hotspot_map = create_hotspot_map_visualization(high_density_locations)
    st.plotly_chart(hotspot_map, width="stretch")