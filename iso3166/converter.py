import os
import pandas as pd


DATA_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         "country_name.csv")
DATA = pd.read_csv(DATA_PATH, dtype=str)


def country_name_conversion(df: pd.DataFrame,
                            *,
                            input_format: str,
                            output_format: str,
                            fuzzy_threshold: int = 0,
                            sample_size: int = 5) -> None:

    """TODO Make validators for input variables"""

    target_column = _auto_found_column(df, input_format, sample_size)

    pass


def _auto_found_column(df: pd.DataFrame, input_format: str, sample_size: int) -> str:

    for col in df.columns:
        for sample in df[col].sample(sample_size):
            if sample in DATA[input_format]:
                return col

    """TODO raise an error and log it, double check time complexity"""


if __name__ == "__main__":
    print(DATA_PATH)