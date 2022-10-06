import os
import pytest
import pandas as pd


@pytest.fixture()
def load_test_data(generate_file_path):
    return pd.read_csv(generate_file_path)


@pytest.fixture()
def generate_file_path():
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/test_data.csv")


@pytest.fixture()
def generate_folder_path():
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/folder_test")
