import os
import time
import random
import io

import pandas as pd
import numpy as np
from functools import lru_cache
from typing import Generator, Callable, Dict, Any

from ..error.exceptions import FileLoadingError, FileSavingError
from ..iso3166.dispatcher import DynamicFileMachine


def read_s3_data(file_name: str, data: io.BytesIO) -> pd.DataFrame:
    """
        ## **Function**
        ----------

        The function reads files byte data of a target s3 bucket and
        converts it into a dataframe.

        ## **Parameters**
        ----------

        `file_name`:
            Name of the file to determine the file type.

        `data`:
            Byte data that gets loaded into a dataframe object.

        `return pd.DataFrame`:
            Returns a pd.DataFrame object that contains data from the s3 file.
        """
    try:
        _, file_type = os.path.splitext(file_name)
        read_function = DynamicFileMachine(file_type).dispatcher()

        return read_function(data)

    except Exception as err:
        raise FileLoadingError(err,
                               message="Error loading following "
                                       "file from s3 bucket")


def load_to_s3(s3_client: Any, destination: str,
               name: str, dataframe: pd.DataFrame) -> None:

    """
    ## **Function**
    ----------

    The function loads a dataframe into a file and stores it in a s3 bucket.

    ## **Parameters**
    ----------

    `s3_client`:
        Boto3 s3 client that is passed in the object handle function.

    `destination`:
        Name of the destination bucket.

    `name`:
        Desired file name after being uploaded into the s3 bucket.

    `dataframe`:
        Dataframe with the prepared data that gets loaded into the file.

    `return None`:
        Returns nothing.
    """

    out_buffer = io.BytesIO()
    dataframe.to_parquet(out_buffer, index=False)
    s3_client.put_object(Bucket=destination,
                         Key=name,
                         Body=out_buffer.getvalue())


def read_data(path: str) -> Generator:
    """
    ## **Function**
    ----------

    The function automatically detects the file format by the given path
    parameter and returns a generator function for the loading of said files.

    ## **Parameters**
    ----------

    `path`:
        The path of the file or folder that needs to be standardized.

    `return Generator`:
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
                _, file_type = os.path.splitext(file_path)

                if not file_type:
                    raise FileLoadingError(err="No file type found")

                # Finds the function that is used to read each file
                read_function = DynamicFileMachine(file_type).dispatcher()

                all_read_functions[file_path] = read_function

            return _read_data(path, all_read_functions)

        # If a file path is given, only finds the function for that one file
        _, file_type = os.path.splitext(path)
        read_function = DynamicFileMachine(file_type).dispatcher()

        return _read_data(path, {path: read_function})

    except Exception as err:
        raise FileLoadingError(err,
                               message=f"Error loading following file: {path}")


def _read_data(path: str,
               format_function: Dict[str, Callable]
               ) -> Generator:
    """
    ## **Function**
    ----------

    Takes in a path and the function directory to create a generator for the
    file or folder.


    ## **Parameters**
    ----------

    `path`:
        The path to the file or folder that contains the data.

    `format_function`:
        The directory that contains the function for each file.

    `Generator`:
        Returns generator with all the data.
    """

    # Checks if the path is a folder
    if os.path.isdir(path) is True:

        # Creates a generator for each file in the folder
        return (format_function[os.path.join(path, f)]
                (os.path.join(path, f)) for f in os.listdir(path))
    else:
        # Quick fix
        return (format_function[path](path) for x in range(0, 1))


@lru_cache(maxsize=None)
def calculate_levenshtein_ratio(base_str: str, target_str: str) -> float:
    """

    ## **Function**
    ----------

    Function calculates the Levenshtein distance ratio between two strings. The
    Levenshtein distance is the minimum number of single digit edits required
    to change a word into another. The ratio of the Levenshtein distance
    shows how similar two strings are. 1.0 meaning that the strings are a
    complete match, while 0.0 means that they don't match at all.

    ## **Parameters**
    ----------

    `base_str`:
        The string which ratio we are finding.

    `target_str`:
        The target string that gets matched against.

    `return float`:
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

    return ((len(base_str) + len(target_str))
            - zero_matrix[row][col]) / (len(base_str) + len(target_str))


def export_to_parquet(path: str, dataframe: pd.DataFrame) -> None:
    """
    ## **Function**
    ----------


    Function writes out a pandas dataframe to parquet format based on the path
    given. If it is a folder, the function creates a new name for the file.
    Otherwise, the file path is used to generate the name.

    ## **Parameters**
    ----------

    `path`:
        Path that is used to create the parquet file. It can be either a folder
        or file path.

    `dataframe`:
        Cleaned dataframe that will be writen in file.

    `return None`:
        Returns nothing
    """

    # Create current timestamp and name
    time_string = time.strftime("%Y%m%d-%H%M%S")
    new_name = "file_export"
    random_id = random.randint(1000, 9999)

    # Check if folder
    if os.path.isdir(path):
        full_path = os.path.join(path, f"{new_name}-{time_string}-{random_id}")

        dataframe.to_parquet(full_path)

    else:
        dataframe.to_parquet(path)


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


def generate_report_template() -> pd.DataFrame:
    """
    ## **Function**
    ----------
    Generates an empty dataframe that is used as a reporting template.

    `return` pd.DataFrame:
        Returns empty dataframe
    """

    report_template = pd.DataFrame({"file_name": [], "column_name": [],
                                    "count_missing": [], "time": []})

    return report_template


def update_reporting(df: pd.DataFrame,
                     report_template: pd.DataFrame,
                     file_name: str,
                     detailed: bool
                     ):
    """
    ## **Function**
    ----------

    Populates the reporting template with the necessary data detailing the
    missing values (not matched countries).

    ## **Parameters**
    ----------

    `df`:
        Dataframe on which the report is based on.

    `report_template`:
        Empty dataframe that is defined out of scope of this function which
        contains the columns needed to the update.

    `file_name`:
        Name of the file from which the data is coming from

    `detailed`:
        Defines the level of detail that needs to be returned. True returns
        the actual row where the data is missing, while False returns a count
        summary.

    `return` pd.DataFrame:
        Returns DataFrame containing the report.
    """
    # Get last two columns
    column_list = df.columns[-2:]

    # Slice dataframe with last two columns
    df = df[column_list]

    # Count missing values and get all None rows
    none_df = df[
        (df[column_list[0]] == "None") | (df[column_list[1]] == "None")
        ]

    if detailed:
        return none_df

    summarization_df = none_df.count()

    # Add new row to summarization
    for name, data in summarization_df.items():
        report_template.loc[-1] = {
            "file_name": file_name,
            "column_name": name,
            "count_missing": data,
            "time": time.strftime("%Y-%m-%d-%H-%M-%S")}

        report_template.index = report_template.index + 1
        report_template = report_template.sort_index()

    return report_template.dropna(axis=0)


def finalize_report(df: pd.DataFrame):
    """
    ## **Function**
    ----------

    Generates name of the file and saves it as a csv in the reports folder.

    ## **Parameters**
    ----------

    `df`:
        Dataframe that contains the report data
    `return`:
        Returns nothing
    """

    if df.empty:
        print("No issues found")

    path = r"chalicelib/reports"

    time_string = time.strftime("%Y%m%d-%H%M%S")
    new_name = "error_report"
    random_id = random.randint(1000, 9999)
    full_path = os.path.join(path, f"{new_name}-{time_string}-{random_id}")

    try:
        df.to_csv(full_path)

    except Exception as err:
        raise FileSavingError(err=err, message="Error saving report")
