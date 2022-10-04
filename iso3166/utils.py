import os
import pandas as pd


def read_data(path: str) -> pd.DataFrame:
    """
    TODO Make this a generator
    """
    # Check if the path is a folder
    if os.path.isdir(path) is True:

        for file in os.listdir(path):
            pass

    return _load_file(path)


def _load_file(path: str) -> pd.DataFrame:

    """ TODO define outcome for no file type, place into try/except block with logger
    TODO define better catch them all function, add more file type loaders"""

    file_functions = {".csv": pd.read_csv}

    # Find file type
    _, file_type = os.path.split(path)

    if file_type is None:
        pass # raise error and log it

    elif file_type in file_functions:
        return file_functions[file_type](path)

    # Excel as a catch them all
    return pd.read_excel(path)


def column_finder(df: pd.DataFrame, conversion_type: str) -> pd.Series:
    pass
