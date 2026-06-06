import pandas as pd
import matplotlib.pyplot as plt


def extract_hour_data(df, hour_column="OCC_HOUR"):
    if hour_column not in df.columns:
        raise KeyError(f"{hour_column} column not found")

    hour_df = df[[hour_column]].copy()

    hour_df[hour_column] = pd.to_numeric(
        hour_df[hour_column],
        errors="coerce"
    )

    hour_df = hour_df.dropna()

    hour_df = hour_df[
        (hour_df[hour_column] >= 0)
        & (hour_df[hour_column] <= 23)
    ]

    hour_df[hour_column] = hour_df[hour_column].astype(int)

    return hour_df


def group_crimes_by_hour(df, hour_column="OCC_HOUR"):
    hour_df = extract_hour_data(df, hour_column)

    hourly_counts = (
        hour_df[hour_column]
        .value_counts()
        .sort_index()
    )

    return hourly_counts


def generate_hourly_summary_table(df, hour_column="OCC_HOUR"):
    hourly_counts = group_crimes_by_hour(df, hour_column)

    summary_table = hourly_counts.reset_index()
    summary_table.columns = ["hour", "crime_count"]

    return summary_table


def create_hourly_crime_visualization(hourly_summary):
    fig, ax = plt.subplots()

    ax.bar(
        hourly_summary["hour"],
        hourly_summary["crime_count"]
    )

    ax.set_title("Crimes by Hour of Day")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Crime Count")

    return fig


def identify_peak_hours(hourly_counts):
    max_count = hourly_counts.max()

    peak_hours = hourly_counts[
        hourly_counts == max_count
    ].index.tolist()

    return peak_hours


def format_hour_range(hour):
    display_hour = hour % 12 or 12
    period = "AM" if hour < 12 else "PM"

    return (
        f"{display_hour}:00 {period} - "
        f"{display_hour}:59 {period}"
    )


def print_hour_legend():
    print("\nHour Legend:")

    for hour in range(24):
        print(f"{hour:>2} = {format_hour_range(hour)}")


if __name__ == "__main__":
    df = pd.read_csv("data/Toronto_Crime_Indicators.csv")

    hourly_counts = group_crimes_by_hour(df)

    print("\nHourly Crime Counts:")
    print(hourly_counts.head())

    summary = generate_hourly_summary_table(df)

    print("\nHourly Summary:")
    print(summary.head())

    print_hour_legend()

    peak_hours = identify_peak_hours(hourly_counts)

    print("\nPeak Crime Hour(s):")

    for hour in peak_hours:
        print(
            f"Hour {hour} "
            f"({format_hour_range(hour)})"
        )