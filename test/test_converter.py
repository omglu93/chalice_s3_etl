import pytest
import pandas as pd
import numpy as np

from iso3166.converter import country_name_conversion
from error.exceptions import AutoDetectionError


def test_country_name_conversion_no_column_name():
    test_df = pd.DataFrame(
        {"messy_country": ["no single", "countries", "here"]})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df)


def test_country_name_conversion_only_primary_column_name():
    test_df = pd.DataFrame(
        {"messy_country": ["Republic of Bulgaria"]})

    return_dataframe = country_name_conversion(test_df)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_only_secondary_column_name():
    test_df = pd.DataFrame(
        {"messy_country": ["BA"]})

    return_dataframe = country_name_conversion(test_df)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_two_column_names():
    test_df = pd.DataFrame(
        {"messy_country": ["Republic of Bulgaria"],
         "messy_code": ["BA"]})

    return_dataframe = country_name_conversion(test_df)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_empty_df():

    test_df = pd.DataFrame(
        {"messy_country": [],
         "messy_code": []})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df)


def test_country_name_conversion_none_types():

    test_df = pd.DataFrame(
        {"messy_country": [np.nan],
         "messy_code": [np.nan]})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df)


def test_country_name_conversion_none_types_in_data():
    test_df = pd.DataFrame(
        {"messy_country": [np.nan, "Canada"],
         "messy_code": ["CA", np.nan]})

    df = country_name_conversion(test_df, fuzzy_threshold=60)

    assert df["country_name_final"][0] == "Canada"
    assert df["country_name_final"][1] == "Canada"
    assert df["country_code_final"][0] == "CA"
    assert df["country_code_final"][1] == "CA"


def test_country_name_conversion_wrong_data_type():
    test_df = pd.DataFrame(
        {"messy_country": [np.nan, 1],
         "messy_code": ["CA", 2]})

    df = country_name_conversion(test_df)
    assert isinstance(df, pd.DataFrame)


def test_country_name_conversion_no_column_name_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": ["no single", "countries", "here"]})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df, fast_mode=False)


def test_country_name_conversion_only_primary_column_name_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": ["Republic of Bulgaria"]})

    return_dataframe = country_name_conversion(test_df, fast_mode=False)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_only_secondary_column_name_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": ["BA"]})

    return_dataframe = country_name_conversion(test_df, fast_mode=False)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_two_column_names_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": ["Republic of Bulgaria"],
         "messy_code": ["BA"]})

    return_dataframe = country_name_conversion(test_df, fast_mode=False)

    assert type(return_dataframe) == pd.DataFrame


def test_country_name_conversion_empty_df_slow_mode():

    test_df = pd.DataFrame(
        {"messy_country": [],
         "messy_code": []})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df, fast_mode=False)


def test_country_name_conversion_none_types_slow_mode():

    test_df = pd.DataFrame(
        {"messy_country": [np.nan],
         "messy_code": [np.nan]})

    with pytest.raises(AutoDetectionError) as e_info:
        country_name_conversion(test_df, fast_mode=False)


def test_country_name_conversion_none_types_in_data_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": [np.nan, "Canada"],
         "messy_code": ["CA", np.nan]})

    df = country_name_conversion(test_df, fast_mode=False)

    assert df["country_name_final"][0] == "Canada"
    assert df["country_name_final"][1] == "Canada"
    assert df["country_code_final"][0] == "CA"
    assert df["country_code_final"][1] == "CA"


def test_country_name_conversion_wrong_data_type_slow_mode():
    test_df = pd.DataFrame(
        {"messy_country": [np.nan, 1],
         "messy_code": ["CA", 2]})

    df = country_name_conversion(test_df, fast_mode=False)
    assert isinstance(df, pd.DataFrame)

