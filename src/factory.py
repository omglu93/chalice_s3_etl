import os

from src import iso3166
from typing import Optional


def name_standardization_factory(input_file_location: str,
                                 output_location: str,
                                 fuzzy_threshold: Optional[int] = 70,
                                 sample_size: Optional[int] = 10,
                                 auto_find_retry: Optional[int] = 3,
                                 fast_mode: Optional[bool] = False,
                                 detailed_report: Optional[bool] = False
                                 ) -> None:
    """
    ## **Function**
    ----------

    Function takes in any number of data files, finds their country/code
    columns, standardizes them to the ISO3166 format (alpha-2 for
    country codes) and exports them to a parquet file and exports them.

    ## **Parameters**
    ----------

    `input_file_location`:
        The path to a file or folder containing multiple files.

    `output_location`:
        The output location where the parquet files will be stored.

    `fuzzy_threshold`:
        The minimum ratio between two strings that is needed to match them.
        For example, an integer of 80 means that the matching ratio needs to be
        above 0.8.
    `sample_size`:
        Integer that defines the sample size used for the auto-detection of
        the columns.

    `auto_find_retry`:
        The number of reties that the function will do for the auto-detection
        of columns

    `detailed_report`:
        Boolean value that determines if the report will contain the summary
        or all the issue data.

    `return None`:
        Returns nothing.
    """

    # Read the path data
    data_generator = iso3166.read_data(path=input_file_location)

    # Create empty report template dataframe
    # Summarization or detailed
    report_template = iso3166.generate_report_template()

    # Check if the location is a file or folder
    try:
        file_list = os.listdir(input_file_location)

    except NotADirectoryError:
        file_list = input_file_location,

    for dataset, filename in zip(data_generator, file_list):

        # Process the data
        dataframe = iso3166.country_name_conversion(
            df=dataset,
            fuzzy_threshold=fuzzy_threshold,
            sample_size=sample_size,
            auto_find_retry=auto_find_retry,
            fast_mode=fast_mode)

        report_template = iso3166.update_reporting(
            dataframe,
            report_template,
            filename,
            detailed_report)

        # Write the data
        iso3166.export_to_parquet(output_location, dataframe)

    # Write report
    iso3166.finalize_report(report_template)
