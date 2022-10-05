import os
import pandas as pd


DATA_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         "country_name.csv")
DATA = pd.read_csv(DATA_PATH, dtype=str)


def country_name_conversion(df: pd.DataFrame,
                            *,
                            input_format: str = "name",
                            fuzzy_threshold: int = 0,
                            sample_size: int = 5) -> None:

    """TODO Make validators for input variables"""

    available_formats = {"name", "official", "alpha-2", "alpha-3"}

    if input_format not in available_formats:
        raise ValueError()

    # Detect column
    target_column = _auto_find_column(df, input_format, sample_size)

    pass


def _auto_find_column(df: pd.DataFrame, input_format: str, sample_size: int) -> str:

    target_column = DATA[input_format].str.lower()
    target_column = target_column.str.replace(" ", "").values

    for col in df.columns:
        for sample in df[col].sample(sample_size):
            if str(sample).lower().strip() in target_column:
                return col

    """TODO raise an error and log it, double check time complexity"""


def _format_country_name(val: str, input_format: str, fuzzy_threshold: int) -> str:

    country = str(val).replace(" ", "").lower()

def _find_country(country: str, input_format: str, fuzzy_threshold: int) -> str:
    pass

if __name__ == "__main__":
    test_df = pd.DataFrame(
        {
            "messy_country": [
                "Canada",
                "foo canada bar",
                "cnada",
                "northern ireland",
                " ireland ",
                "Denmark"]
        })

    x = _auto_find_column(test_df, "name", 5)
    print(x)
    print("Done")
