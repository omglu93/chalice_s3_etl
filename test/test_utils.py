import types

import pandas as pd

from iso3166.utils import read_data
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
