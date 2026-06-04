import pandas as pd
import pytest

from src.data_loader import load_dataset
from src.data_loader import get_record_count


def test_load_dataset_returns_dataframe(tmp_path):
    test_file = tmp_path / "sample.csv"

    test_file.write_text(
        "id,name\n"
        "1,John\n"
        "2,Mary\n"
    )

    df = load_dataset(test_file)

    assert isinstance(df, pd.DataFrame)


def test_get_record_count():
    df = pd.DataFrame({
        "id": [1, 2, 3]
    })

    assert get_record_count(df) == 3


def test_load_dataset_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset("missing_file.csv")