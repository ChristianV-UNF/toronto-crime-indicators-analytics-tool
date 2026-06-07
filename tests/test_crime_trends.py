import pandas as pd
from src.crime_trends import (
    prepare_datetime,
    extract_time_features,
    get_monthly_trend,
    get_yearly_trend,
    get_month_over_month_change,
    generate_trend_summary,
)


def sample_data():
    return pd.DataFrame({
        "OCC_DATE": [
            "2020-01-01",
            "2020-01-15",
            "2020-02-10",
            "2021-01-01",
            "2021-02-01",
            "2022-03-01"
        ]
    })


def test_prepare_datetime():
    df = prepare_datetime(sample_data())

    assert "OCC_DATE" in df.columns

    assert pd.api.types.is_datetime64_any_dtype(df["OCC_DATE"])


def test_extract_time_features():
    df = extract_time_features(prepare_datetime(sample_data()))

    assert "year_month" in df.columns

    assert pd.api.types.is_datetime64_any_dtype(df["year_month"])


def test_monthly_trend():
    df = extract_time_features(prepare_datetime(sample_data()))
    result = get_monthly_trend(df)

    assert "crime_count" in result.columns
    assert len(result) > 0


def test_yearly_trend():
    df = extract_time_features(prepare_datetime(sample_data()))
    result = get_yearly_trend(df)

    assert "crime_count" in result.columns
    assert len(result) > 0


def test_month_over_month_change():
    df = extract_time_features(prepare_datetime(sample_data()))
    result = get_month_over_month_change(df)

    assert "change" in result.columns
    assert "percent_change" in result.columns


def test_trend_summary():
    df = extract_time_features(prepare_datetime(sample_data()))
    summary = generate_trend_summary(df)

    assert "trend" in summary
    assert "insight" in summary