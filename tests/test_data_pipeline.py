import pandas as pd

from src.data_pipeline import load_clean_validate_dataset, get_clean_dataset


def test_load_clean_validate_dataset_returns_expected_keys(tmp_path):
    test_file = tmp_path / "test_data.csv"

    df = pd.DataFrame({
        "OBJECTID": [1, 2],
        "EVENT_UNIQUE_ID": ["A", "B"],
        "REPORT_DATE": ["1/1/2020 5:00:00 AM", "1/2/2020 5:00:00 AM"],
        "OCC_DATE": ["1/1/2020 5:00:00 AM", "1/2/2020 5:00:00 AM"],
        "OCC_HOUR": [1, 2],
        "LAT_WGS84": [43.65, 43.66],
        "LONG_WGS84": [-79.38, -79.39],
        "NEIGHBOURHOOD_158": ["Test Area", "Test Area"],
    })

    df.to_csv(test_file, index=False)

    result = load_clean_validate_dataset(str(test_file))

    assert "raw_df" in result
    assert "cleaned_df" in result
    assert "validation_report" in result
    assert isinstance(result["raw_df"], pd.DataFrame)
    assert isinstance(result["cleaned_df"], pd.DataFrame)
    assert isinstance(result["validation_report"], dict)


def test_get_clean_dataset_returns_dataframe(tmp_path):
    test_file = tmp_path / "test_data.csv"

    df = pd.DataFrame({
        "OBJECTID": [1],
        "EVENT_UNIQUE_ID": ["A"],
        "REPORT_DATE": ["1/1/2020 5:00:00 AM"],
        "OCC_DATE": ["1/1/2020 5:00:00 AM"],
        "OCC_HOUR": [1],
        "LAT_WGS84": [43.65],
        "LONG_WGS84": [-79.38],
        "NEIGHBOURHOOD_158": ["Test Area"],
    })

    df.to_csv(test_file, index=False)

    result = get_clean_dataset(str(test_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1


def test_pipeline_removes_invalid_coordinate_records(tmp_path):
    test_file = tmp_path / "test_data.csv"

    df = pd.DataFrame({
        "OBJECTID": [1, 2],
        "EVENT_UNIQUE_ID": ["A", "B"],
        "REPORT_DATE": ["1/1/2020 5:00:00 AM", "1/2/2020 5:00:00 AM"],
        "OCC_DATE": ["1/1/2020 5:00:00 AM", "1/2/2020 5:00:00 AM"],
        "OCC_HOUR": [1, 2],
        "LAT_WGS84": [43.65, 999],
        "LONG_WGS84": [-79.38, -999],
        "NEIGHBOURHOOD_158": ["Test Area", "Test Area"],
    })

    df.to_csv(test_file, index=False)

    result = get_clean_dataset(str(test_file))

    assert len(result) == 1