import iso3166
from typing import Optional


def name_standardization_factory(input_file_location: str,
                                 output_location: str,
                                 fuzzy_threshold: Optional[int] = 70,
                                 sample_size: Optional[int] = 10,
                                 auto_find_retry: Optional[int] = 3) -> None:
    """
    Function takes in any number of data files, finds their country/code
    columns, standardizes them to the ISO3166 format (alpha-2 for
    country codes) and exports them to a parquet file and exports them.

    Parameters
    ----------

    :param input_file_location:
        The path to a file or folder containing multiple files.
    :param output_location:
        The output location where the parquet files will be stored.
    :param fuzzy_threshold:
        The minimum ratio between two strings that is needed to match them.
        For example, an integer of 80 means that the matching ratio needs to be
        above 0.8.
    :param sample_size:
        Integer that defines the sample size used for the auto-detection of
        the columns.
    :param auto_find_retry:
        The number of reties that the function will do for the auto-detection
        of columns
    :return None:
        Returns nothing.
    """

    # Read the path data
    data_generator = iso3166.read_data(path=input_file_location)

    for dataset in data_generator:
        # Process the data
        dataframe = iso3166.country_name_conversion(
            df=dataset,
            fuzzy_threshold=fuzzy_threshold,
            sample_size=sample_size,
            auto_find_retry=auto_find_retry
        )
        # Write the data
        iso3166.export_to_parquet(output_location, dataframe)


if __name__ == "__main__":
    name_standardization_factory(r"/Users/omargluhic/PycharmProjects/dataeng_task/test/test_data/folder_test",
                                 r"/Users/omargluhic/PycharmProjects/dataeng_task/test/test_data/output_test")
