import pytest
import pandas as pd

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
