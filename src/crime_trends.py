import pandas as pd
import plotly.express as px

#import matplotlib.pyplot as plt

# ----------------------------
# DATA PREPARATION
# ----------------------------

def prepare_datetime(df: pd.DataFrame, date_column: str = "OCC_DATE") -> pd.DataFrame:
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    df = df.dropna(subset=[date_column])
    return df


def extract_time_features(df: pd.DataFrame, date_column: str = "OCC_DATE") -> pd.DataFrame:
    df = df.copy()
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month

    df["year_month"] = df[date_column].dt.to_period("M").dt.to_timestamp()

    return df


# ----------------------------
# TREND ANALYSIS
# ----------------------------

def get_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    trend = (
        df.groupby("year_month")
        .size()
        .reset_index(name="crime_count")
        .sort_values("year_month")
    )

    return trend


def get_yearly_trend(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("year")
        .size()
        .reset_index(name="crime_count")
        .sort_values("year")
    )


def get_month_over_month_change(df: pd.DataFrame) -> pd.DataFrame:
    trend = get_monthly_trend(df).copy()

    trend["change"] = trend["crime_count"].diff()
    trend["percent_change"] = trend["crime_count"].pct_change() * 100

    return trend


# ----------------------------
# INSIGHT GENERATION
# ----------------------------

def generate_trend_summary(df: pd.DataFrame) -> dict:
    yearly = get_yearly_trend(df)

    if len(yearly) < 2:
        return {
            "trend": "Insufficient data",
            "insight": "Not enough historical data for trend analysis."
        }

    start_year = int(yearly.iloc[0]["year"])
    end_year = int(yearly.iloc[-1]["year"])

    start = yearly.iloc[0]["crime_count"]
    end = yearly.iloc[-1]["crime_count"]

    if end > start:
        trend = "Increasing"
    elif end < start:
        trend = "Decreasing"
    else:
        trend = "Stable"

    #change = ((end - start) / start) * 100 if start != 0 else 0
    absolute_change = end - start
    percent_change = ((end - start) / start) * 100 if start != 0 else 0

    return {
    "trend": trend,
    "start_year": start_year,
    "end_year": end_year,
    "absolute_change": int(absolute_change),
    "percent_change": round(percent_change, 2),
    "insight": (
        f"Crime is {trend.lower()} by {int(absolute_change)} cases "
        f"({round(percent_change,2)}%) from {start_year} to {end_year}."
    )
}


# ----------------------------
# VISUALIZATION
# ----------------------------

def plot_monthly_trend(df: pd.DataFrame):
    trend = get_monthly_trend(df)

    fig = px.line(
        trend,
        x="year_month",
        y="crime_count",
        markers=True,
        title="Crime Trends Over Time (Monthly)"
    )

    fig.update_layout(
        xaxis_title="Year-Month",
        yaxis_title="Number of Crimes",
        xaxis=dict(tickangle=45),
        template="plotly_white"
    )

    return fig
