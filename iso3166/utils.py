import os
import pandas as pd
import numpy as np

from typing import Generator
from error.exceptions import FileLoadingError


def read_data(path: str) -> Generator:

    try:
        # Check if the path is a folder
        if os.path.isdir(path) is True:
            for file in os.listdir(path):
                yield _load_file(os.path.join(path, file))
        yield _load_file(path)

    except Exception as error:
        FileLoadingError(str(error), message="Error loading files")


def _load_file(path: str) -> pd.DataFrame:
    """ TODO define outcome for no file type, place into try/except block with logger
    TODO define better catch them all function, add more file type loaders"""

    file_functions = {".csv": pd.read_csv}

    # Find file type
    _, file_type = os.path.splitext(path)

    if file_type is None:
        raise FileLoadingError("File format not found")

    elif file_type in file_functions:
        return file_functions[file_type](path)

    # Excel as a catch them all
    return pd.read_excel(path)


def calculate_levenshtein_ratio(base_str: str, target_str: str) -> float:
    # Create matrix
    rows = len(base_str) + 1
    cols = len(target_str) + 1

    zero_matrix = np.zeros((rows, cols), dtype=int)

    # Populate matrix with characters of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            zero_matrix[i][0] = i
            zero_matrix[0][k] = k

    # Find cost of substitution
    for col in range(1, cols):
        for row in range(1, rows):
            if base_str[row - 1] == target_str[col - 1]:
                cost = 0
            else:
                cost = 2

            # Cost of deletion, insertion and substitution
            zero_matrix[row][col] = min(zero_matrix[row - 1][col] + 1,
                                        zero_matrix[row][col - 1] + 1,
                                        zero_matrix[row - 1][col - 1] + cost)

    return ((len(base_str)+len(target_str)) - zero_matrix[row][col]) / (len(base_str)+len(target_str))


if __name__ == "__main__":
    BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    LOG_PATH = f"{BASE_PATH}/log/base_loger.log"
    x = calculate_levenshtein_ratio("canada", "cnada")
    print(x)
    print(LOG_PATH)