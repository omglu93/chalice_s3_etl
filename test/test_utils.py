import types
import pytest
import pandas as pd

from iso3166.utils import read_data, calculate_levenshtein_ratio
from fixtures import generate_file_path, generate_folder_path


def test_read_data_file(generate_file_path):

    data = read_data(generate_file_path)

    assert isinstance(data, types.GeneratorType)
    assert type(next(data)) == pd.DataFrame


def test_read_data_folder(generate_folder_path):

    data = read_data(generate_folder_path)

    assert isinstance(data, types.GeneratorType)
    assert type(next(data)) == pd.DataFrame
    assert type(next(data)) == pd.DataFrame


def test_read_data_file_exception_int():
    with pytest.raises(Exception) as e_info:
        data = read_data(12)


def test_read_data_file_exception_wrong_path():
    with pytest.raises(Exception) as e_info:
        data = read_data("/not/ok/path")


def test_read_data_folder_exception_int():
    with pytest.raises(Exception) as e_info:
        data = read_data(12)


def test_read_data_folder_exception_wrong_path():
    with pytest.raises(Exception) as e_info:
        data = read_data("/not/ok/path")


def test_levenshtein_calculation_perf_match():

    base = "Canada"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x == 1


def test_levenshtein_calculation_close_match():

    base = "Canaaada"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x >= 0.9


def test_levenshtein_calculation_no_match():

    base = "nothing"
    target = "Canada"

    x = calculate_levenshtein_ratio(base, target)

    assert x <= 0.5
