import os
import pytest
import pandas as pd


@pytest.fixture()
def load_test_data(generate_file_path):
    """
    Fixture function that reads and returns a pandas Dataframe for testing.
    :param generate_file_path:
        Fixture function that generates a dynamic file path.
    :return pd.DataFrame:
        Returns a pandas dataframe.
    """

    return pd.read_csv(generate_file_path)


@pytest.fixture()
def generate_file_path():
    """
    Fixture function that returns a dynamic string.
    :return str:
        Returns a string of a file path.
    """
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/test_data.csv")


@pytest.fixture()
def generate_folder_path():
    """
    Fixture function that returns a dynamic string of a folder
    :return:
        Returns a string of a folder path.
    """
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/folder_test")


@pytest.fixture()
def generate_output_folder_path():
    """
    Fixture function that returns a dynamic string of a folder
    :return:
        Returns a string of a folder path.
    """
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/output_test")


@pytest.fixture()
def generate_example_file_path():
    """
    Fixture function that returns a dynamic string of an example file.
    :return str:
        Returns a string of a file path.
    """
    return os.path.join(os.path.split(os.path.abspath(__file__))[0],
                        "test_data/population_by_country_2020.csv")
