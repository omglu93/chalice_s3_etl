import os
import pandas as pd

from iso3166.utils import calculate_levenshtein_ratio
from error.exceptions import DistanceCalculationError, AutoDetectionError

DATA_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         "country_name.csv")
DATA = pd.read_csv(DATA_PATH, dtype=str)


def country_name_conversion(df: pd.DataFrame,
                            *,
                            fuzzy_threshold: int = 55,
                            sample_size: int = 10,
                            auto_find_retry: int = 3) -> pd.DataFrame:
    # Detect column
    target_column = None
    secondary_column = None
    ini_num_col = len(df.columns)

    for i in range(auto_find_retry):
        target_column = _auto_find_column(df, "official", sample_size)
        if target_column is not None:
            break
    try:
        df["country_name"] = df[target_column].apply(
            _format_country_name,
            args=("official", fuzzy_threshold, "official"))
        df["country_code"] = df[target_column].apply(
            _format_country_name, args=("official", fuzzy_threshold, "alpha-2"))

    except KeyError as err:
        AutoDetectionError(err=err, message="Program cannot autodetect columns")

    try:
        for i in range(auto_find_retry):
            secondary_column = _auto_find_column(df, "alpha-2", sample_size)
            if secondary_column is not None:
                break

        df["country_code_helper"] = df[secondary_column].apply(
            _format_country_name, args=("alpha-2", fuzzy_threshold, "alpha-2"))
        df["country_name_helper"] = df[secondary_column].apply(
            _format_country_name, args=("alpha-2", fuzzy_threshold, "official"))

    except KeyError as err:
        AutoDetectionError(err=err, message="Program cannot autodetect columns")

    if all(col is None for col in (target_column, secondary_column)):
        raise AutoDetectionError("Program cannot autodetect columns")

    elif not [col for col in (target_column, secondary_column) if col is None]:
        # improves accuracy with a small amount of overhead
        df["country_name_final"] = df["country_name"].combine_first(
            df.country_name_helper)
        df["country_code_final"] = df["country_code"].combine_first(
            df.country_code_helper)

    # Dynamic column drop

    # We always want to keep the last two
    final_num_col = len(df.columns) - 2
    df.drop(df.columns[[col for col in range(ini_num_col, final_num_col)]],
            axis=1,
            inplace=True)

    return df


def _auto_find_column(df: pd.DataFrame, input_format: str,
                      sample_size: int) -> str:
    target_column = DATA[input_format].str.lower()
    target_column = target_column.str.replace(" ", "").values

    # Overwrite sample size if it's larger than the dataset
    if len(df) < sample_size:
        sample_size = len(df)

    for col in df.columns:
        for sample in df[col].sample(sample_size):
            if str(sample).lower().replace(" ", "") in target_column:
                return col


def _format_country_name(val: str, input_format: str, fuzzy_threshold: int,
                         wanted_output: str):
    country = str(val).replace(" ", "").lower()

    target_column = DATA[input_format].str.lower()
    target_column = target_column.str.replace(" ", "")

    if country in target_column.values:
        value_index = target_column[target_column == country].index[0]
        return DATA[wanted_output][value_index]

    country_index = _find_best_distance(country, target_column, fuzzy_threshold)

    if country_index is None:
        return None

    return DATA[wanted_output][country_index]


def _find_best_distance(country: str, target_column: pd.Series,
                        fuzzy_threshold: int):
    results = []

    for i, val in enumerate(target_column):

        try:
            match_ratio = calculate_levenshtein_ratio(country, val)
            if match_ratio >= fuzzy_threshold / 100:
                results.append((match_ratio, i))

        except Exception as err:

            DistanceCalculationError(err=err,
                                     message="Error calculating distance"
                                             f"for:{val} on index {i}")

    if not results:
        """TODO Reporting tool without raising anything"""
        return None
    return max(results)[1]


if __name__ == "__main__":
    test_df = pd.DataFrame(
        {
            "messy_country": [
                "Canada",
                "foo canada bar",
                "cnada",
                "northern ireland",
                " ireland ",
                "this is not a country dude",
                "bosnia and hercegovina",
                "United Kingdom of Great Britain and Northern Ireland",
                "The Federal Republic of Germany"],

            "mess_codes": [
                "CA",
                "ca",
                "ca",
                "GB",
                "IEE",
                "BA",
                "BA",
                "GBB",
                "DA"
            ],

            "numbers": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9
            ]
        })

    # x = _auto_find_column(test_df, "name", 5)
    # y = _find_best_distance("Canadda", "name", 80)
    # z = _format_country_name("Cannnada", "name", 95)
    # g = country_name_conversion(test_df, fuzzy_threshold=80)
    # x = country_name_conversion(test_df)
    # print(x)
    import json
    x = DATA.to_dict("index")
    print(x)
