from .logger import logging


class BaseCustomException(Exception):

    """
    Base exception call used as a parent for more specific exceptions.
    """

    def __init__(self, err=None, message=""):
        self.message = message
        self.err = err
        super().__init__(self.message)

        logging.error(f"{self.message} : {self.err}")

    def __str__(self):
        return self.message


class FileLoadingError(BaseCustomException):
    """
    Exception used for all kinds of errors relating to file loadings.
    """
    pass


class DistanceCalculationError(BaseCustomException):
    """
    Exception used for all kinds of errors relating to the calculation
    of the Levenshtein distance.
    """
    pass


class AutoDetectionError(BaseCustomException):
    """
    Exception used for all kinds of errors relating to the automatic detection
    of columns.
    """
    pass

