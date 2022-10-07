import os
import time

import pandas as pd
import numpy as np
from functools import lru_cache

from typing import Generator, Callable, Dict
from error.exceptions import FileLoadingError


def read_data(path: str) -> Generator:

    if os.path.exists(path) is not True:
        raise FileLoadingError(f"Error - file does not exist for path {path}")

    try:
        if os.path.isdir(path) is True:

            # Validate files and pick functions
            all_read_functions = {}
            for i, file in enumerate(os.listdir(path)):

                file_path = os.path.join(path, file)
                read_function = _find_file_function(file_path)

                all_read_functions[file_path] = read_function
            return _read_data(path, all_read_functions)

        read_function = _find_file_function(path)

        """TODO Find a better way to do this"""
        return _read_data(path, {path: read_function})

    except Exception as err:
        raise FileLoadingError(err, message=f"Error loading following file: {path}")


def _read_data(path: str,
               format_function: Dict[str, Callable]
               ) -> Generator:

    if os.path.isdir(path) is True:
        print("")
        return (format_function[os.path.join(path, f)](os.path.join(path, f)) for f in os.listdir(path))

    yield format_function[path](path)


def _find_file_function(path: str) -> Callable:
    """ TODO define outcome for no file type, place into try/except block with logger
    TODO define better catch them all function, add more file type loaders"""

    file_functions = {".csv": pd.read_csv}
    # Find file type
    _, file_type = os.path.splitext(path)

    try:

        if file_type is None:
            raise FileLoadingError(f"File format not found: {file_type} in {path}")

        elif file_type in file_functions:
            return file_functions[file_type]

        # Excel as a catch them all
        return pd.read_excel

    except Exception as error:
        FileLoadingError(str(error), message="Error loading files")
        raise


@lru_cache(maxsize=None)
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


def timeit(func):
    """
    Decorator for measuring function's running time.
    """
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result

    return measure_time

if __name__ == "__main__":
    x = read_data(r"/Users/omargluhic/PycharmProjects/dataeng_task/test/test_data/folder_test")
    print(next(x))
