import os

import pandas as pd

import factory
from fixtures import generate_file_path, generate_folder_path, \
    generate_output_folder_path, generate_example_file_path


def test_name_stand_factory_file_input(generate_file_path,
                                       generate_output_folder_path):
    factory.name_standardization_factory(generate_file_path,
                                         generate_output_folder_path)

    file_list = os.listdir(generate_output_folder_path)
    assert len(file_list) == 1

    for f in file_list:
        os.remove(os.path.join(generate_output_folder_path, f))


def test_name_stand_factory_folder_input(generate_folder_path,
                                         generate_output_folder_path):
    factory.name_standardization_factory(generate_folder_path,
                                         generate_output_folder_path)

    file_list = os.listdir(generate_output_folder_path)

    for f in file_list:
        os.remove(os.path.join(generate_output_folder_path, f))

    assert len(file_list) == 2


def test_name_stand_factory(generate_output_folder_path,
                            generate_example_file_path):

    factory.name_standardization_factory(generate_example_file_path,
                                         generate_output_folder_path)

    file_name = os.listdir(generate_output_folder_path)[0]
    file_path = os.path.join(generate_output_folder_path, file_name)

    df = pd.read_parquet(file_path)
    """TODO Return to this and add more assertions"""
    assert type(df) == pd.DataFrame
