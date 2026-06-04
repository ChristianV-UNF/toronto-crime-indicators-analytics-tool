import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the Toronto Crime Indicators dataset from a CSV file.

    Args:
        file_path (str): Path to the dataset file.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the file cannot be found.
    """
    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )


def get_record_count(df: pd.DataFrame) -> int:
    """
    Return the total number of records in the dataset.
    """
    return len(df)