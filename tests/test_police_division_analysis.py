# tests/test_police_division_analysis.py
import pandas as pd
import pytest
from matplotlib.figure import Figure

from src.police_division_analysis import (
    group_crimes_by_division,
    calculate_division_crime_counts,
    identify_top_divisions,
    generate_division_rankings,
    create_division_visualization,
)

@pytest.fixture
def sample_division_df():
    return pd.DataFrame({
        "DIVISION": ["D14", "D14", "D31", "D31", "D31", "NSA"]
    })