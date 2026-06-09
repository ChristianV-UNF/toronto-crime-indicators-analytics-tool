import pandas as pd

from src.dashboard import (
    filter_dataset,
    get_dashboard_summary,
)


def test_filter_dataset_by_hour():
    df = pd.DataFrame({
        "OCC_HOUR": [0, 1, 2, 3],
        "OFFENCE": ["A", "B", "C", "D"]
    })

    result = filter_dataset(df, selected_hours=[1, 2])

    assert list(result["OCC_HOUR"]) == [1, 2]


def test_filter_dataset_by_offence():
    df = pd.DataFrame({
        "OCC_HOUR": [0, 1, 2],
        "OFFENCE": ["Assault", "Robbery", "Assault"]
    })

    result = filter_dataset(df, selected_offences=["Assault"])

    assert len(result) == 2
    assert all(result["OFFENCE"] == "Assault")


def test_get_dashboard_summary():
    df = pd.DataFrame({
        "OFFENCE": ["Assault", "Robbery", "Assault"],
        "OCC_HOUR": [0, 1, 2]
    })

    summary = get_dashboard_summary(df)

    assert summary["total_records"] == 3
    assert summary["unique_offences"] == 2