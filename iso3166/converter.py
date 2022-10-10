import os
from typing import Tuple

import pandas as pd
import numpy as np

from iso3166.utils import calculate_levenshtein_ratio
from error.exceptions import DistanceCalculationError, AutoDetectionError

# Loads the csv file containing possible naming options and
# standard naming options for the iso3166 naming standard
DATA_PATH = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         "country_name.csv")
DATA = pd.read_csv(DATA_PATH, dtype=str, keep_default_na=False)


def country_name_conversion(df: pd.DataFrame,
                            *,
                            fuzzy_threshold: int = 70,
                            sample_size: int = 10,
                            auto_find_retry: int = 3,
                            fast_mode: bool = True) -> pd.DataFrame:
    """
    Function cleans and standardizes country names based on the
    iso3166 standard. The output contains the dataframe used as input in
    addition to the two generated columns with the iso3166 country name and code

    Note - the iso3166 country code is based on the alpha-2 option.

    Parameters
    ----------
    :param df:
        A pandas dataframe that contains the data that needs to be cleaned.
    :param fuzzy_threshold:
        The minimum ratio between two strings that is needed to match them.
        For example, an integer of 80 means that the matching ratio needs to be
        above 0.8
    :param sample_size:
        Integer that defines the sample size used for the auto-detection of
        the columns.
    :param auto_find_retry:
        The number of reties that the function will do for the auto-detection
        of columns
    :param fast_mode:
        Boolean value that determines the mode of the application.
            - True - Fast mode only finds one column for the country name
                    and leaves it at that.
            - False - Loops over both the official and unofficial naming
                    before returning results.
    :return pd.Dataframe:
        Returns a cleaned dataframe with iso3166 columns for the country code
        and the country name

    """

    # Column auto-detection
    target_column = None
    secondary_column = None
    ini_num_col = len(df.columns)

    # Temp fix
    option = None

    # Number of retries
    for i in range(auto_find_retry):

        # First tries to match on the normal column, then the official
        for option in ("official", "name"):
            target_column = _auto_find_column(df, option, sample_size)
            if target_column is not None:
                # if the column in found the loop breaks
                break

    # Starts the creation of the helper columns
    try:

        data_column = (DATA[option].str.lower().str.replace(" ", "").values,)

        if not fast_mode:
            # Get columns not chosen
            other = DATA[[x for x in ("official", "name") if x != option][0]] \
                .str.lower().str.replace(" ", "").values
            # Pack both of the Series up
            data_column = (data_column[0],
                           other)

        df["country_name"] = df[target_column].apply(
            _format_country_name,
            args=(data_column,
                  fuzzy_threshold, "official", fast_mode))

        df["country_code"] = df[target_column].apply(
            _format_country_name,
            args=(data_column,
                  fuzzy_threshold, "alpha-2", fast_mode))

    # Catch in case the auto-column finder returns nothing
    except KeyError as err:
        AutoDetectionError(err=err, message="Program cannot autodetect"
                                            " country name columns")

    # Starts the secondary (country code) auto-column search
    try:
        for i in range(auto_find_retry):
            secondary_column = _auto_find_column(df, "alpha-2", sample_size)
            if secondary_column is not None:
                break

        sec_data_col = DATA["alpha-2"].str.lower().str.replace(" ", "").values,

        df["country_code_helper"] = df[secondary_column].apply(
            _format_country_name,
            args=(sec_data_col,
                  fuzzy_threshold, "alpha-2"))

        df["country_name_helper"] = df[secondary_column].apply(
            _format_country_name,
            args=(sec_data_col,
                  fuzzy_threshold, "official"))

    # Catch in case the auto-column finder returns nothing
    except KeyError as err:
        AutoDetectionError(err=err, message="Program cannot autodetect"
                                            " code columns")

    # If no columns are found raises this exception
    if all(col is None for col in (target_column, secondary_column)):
        raise AutoDetectionError("Program cannot autodetect any columns")

    elif not [col for col in (target_column, secondary_column) if col is None]:
        # improves accuracy with a small amount of overhead
        # if both primary and secondary columns where found and used
        # this segment combines the columns to minimize NaN values
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
    # Convert type to string to prevent some parquet errors
    conversion_list = df.columns[[col for col in range(ini_num_col,
                                                       len(df.columns))]]

    df[conversion_list] = df[conversion_list].astype(str)

    return df


def _auto_find_column(df: pd.DataFrame,
                      input_format: str,
                      sample_size: int) -> str | None:
    """
    Private function used to auto-detect the required columns in a dataframe.
    The function takes a sample of each column and tries to match it to the
    input_format.

    Parameters
    ----------

    :param df:
        A pandas dataframe that contains the data.
    :param input_format:
        The format the column finder is looking for. There are three choices
        to it:
            - name - Normal name of the country
            - official - ISO-3166 country name
            - alpha-2 - ISO-3166 country code
    :param sample_size:
        Sample size that the function will match against.
    :return str | None:
        The function returns a column name if there is a match. If not, it
        returns nothing and the error gets picked up by the try except block.
    """

    # Data preparation
    target_column = DATA[input_format].str.lower()
    target_column = target_column.str.replace(" ", "").values

    # Overwrite sample size if it's larger than the dataset
    if len(df) < sample_size:
        sample_size = len(df)

    # Search for the match
    """ TODO Possible update depending on examples given
    1. Add a distance calculation """
    for col in df.columns:
        for sample in df[col].sample(sample_size):
            if str(sample).lower().replace(" ", "") in target_column:
                return col


def _format_country_name(val: str,
                         target_column: tuple[pd.Series],
                         fuzzy_threshold: int,
                         wanted_output: str,
                         fast_mode: bool = True) -> str | None:
    """
    Function re-formats/standardizes the country name.

    Parameters
    ----------

    :param val:
        The target value (country) that needs to be replaced/standardized.
    :param target_column:
        The column that contains the desired formatting.
    :param fuzzy_threshold:
        The fuzzy ratio that decides if a value is replaced or not.
    :param wanted_output:
        The desired output of the formatting.
    :return str | None:
        Returns the formatted string or a None value if the string couldn't be
        matched against any anything.
    """

    # Data preparation
    country = str(val).replace(" ", "").lower()

    # Quick return, if the countries name matches completely
    for data in target_column:
        if country in data[0]:
            value_index = np.where(data[0] == country)[0]
            return DATA[wanted_output][value_index]

    # Calculates the levenshtein ratio and returns index of best value
    if not fast_mode:

        results = []
        for data in target_column:
            country_ratio = _find_best_distance(country, data,
                                                fuzzy_threshold,
                                                ratio=True)
            results.append(country_ratio)

        # Finds the maximum value within a tuple
        max_ratio = 0
        country_index = None
        for match_ratio in results:

            if not match_ratio:
                continue
            if match_ratio[0] > max_ratio:
                max_ratio, country_index = match_ratio

    else:
        country_index = _find_best_distance(country,
                                            target_column[0], fuzzy_threshold)

    if country_index is None:
        return None

    return DATA[wanted_output][country_index]


def _find_best_distance(country: str, target_column: pd.Series,
                        fuzzy_threshold: int,
                        ratio: bool = False) -> None | tuple[float, int] | int:
    """
    Function finds the maximum levenshtein ratio and returns the index of that
    value.

    Parameters
    ----------

    :param country:
        The value whose levenshtein ratio is being calculated.
    :param target_column:
        The column which is being calculated against
    :param fuzzy_threshold:
        The minimum threshold for a value to be considered in the results
    :return int | None:
        returns either the index of the best value or None if a value for the
        given criteria could not be found.
    """
    results = []

    # Calculates the ratio for each value in a given column
    for i, val in enumerate(target_column):

        try:
            match_ratio = calculate_levenshtein_ratio(country, val)
            # If the ratio is higher than the threshold it gets considered
            if match_ratio >= fuzzy_threshold / 100:
                results.append((match_ratio, i))

        except Exception as err:
            DistanceCalculationError(err=err,
                                     message="Error calculating distance"
                                             f"for:{val} on index {i}")

    if not results:
        """TODO Reporting tool without raising anything"""
        return None

    if ratio:
        return max(results)

    return max(results)[1]
