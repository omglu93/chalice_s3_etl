import os
import time

import pandas as pd
import numpy as np
from functools import lru_cache

from typing import Generator, Callable, Dict
from error.exceptions import FileLoadingError


def read_data(path: str) -> Generator:

    """
    The function automatically detects the file format by the given path
    parameter and returns a generator function for the loading of said files.

    Parameters
    ----------

    :param path:
        The path of the file or folder that needs to be standardized.
    :return Generator:
        Returns a generator function that loads the data.
    """

    # Check if path exits
    if os.path.exists(path) is not True:
        raise FileLoadingError(f"Error - file does not exist for path {path}")

    # Check if path is a folder or a file
    try:
        if os.path.isdir(path) is True:

            # Validate files and pick functions
            all_read_functions = {}
            for i, file in enumerate(os.listdir(path)):

                file_path = os.path.join(path, file)
                # Finds the function that is used to read each file
                read_function = _find_file_function(file_path)

                all_read_functions[file_path] = read_function
            return _read_data(path, all_read_functions)

        # If a file path is given, only finds the function for that one file
        read_function = _find_file_function(path)

        return _read_data(path, {path: read_function})

    except Exception as err:
        raise FileLoadingError(err,
                               message=f"Error loading following file: {path}")


def _read_data(path: str,
               format_function: Dict[str, Callable]
               ) -> Generator:
    """
    Takes in a path and the function directory to create a generator for the
    file or folder.

    Note - the function and generator had to be separated as generator don't
    support raising of exceptions.

    Parameters
    ----------
    :param path:
        The path to the file or folder that contains the data.
    :param format_function:
        The directory that contains the function for each file.
    :return Generator:
        Returns generator with all the data.
    """

    # Checks if the path is a folder
    if os.path.isdir(path) is True:

        # Creates a generator for each file in the folder
        return (format_function[os.path.join(path, f)]
                (os.path.join(path, f)) for f in os.listdir(path))

    yield format_function[path](path)


def _find_file_function(path: str) -> Callable:

    """
    The function finds the format of the given path and returns the appropriate
    function to read that file.

    Note - for now we only support csv files and Excel files as a catch all.

    Parameters
    ----------
    :param path:
        Path of the file that needs to be read.
    :return Callable:
        Returns the function needed to read the file.
    """

    """TODO define better catch them all function, add more file type loaders"""

    file_functions = {".csv": pd.read_csv}

    # Find file type
    _, file_type = os.path.splitext(path)

    try:
        if file_type is None:
            raise FileLoadingError("File format not found:"
                                   f" {file_type} in {path}")

        elif file_type in file_functions:
            return file_functions[file_type]

        # Excel as a catch them all
        return pd.read_excel

    except Exception as error:
        FileLoadingError(str(error), message="Error loading files")
        raise


@lru_cache(maxsize=None)
def calculate_levenshtein_ratio(base_str: str, target_str: str) -> float:

    """
    Function calculates the Levenshtein distance ratio between two strings. The
    Levenshtein distance is the minimum number of single digit edits required
    to change a word into another. The ratio of the Levenshtein distance
    shows how similar two strings are. 1.0 meaning that the strings are a
    complete match, while 0.0 means that they don't match at all.

    Parameters
    ----------
    :param base_str:
        The string which ratio we are finding.
    :param target_str:
        The target string that gets matched against.
    :return float:
        Returns a float representing ratio of the match.
    """
    # Create matrix

    rows = len(base_str) + 1
    cols = len(target_str) + 1

    row = None
    col = None

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

    return ((len(base_str)+len(target_str))
            - zero_matrix[row][col]) / (len(base_str)+len(target_str))


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
