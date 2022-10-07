from .logger import logging


class BaseCustomException(Exception):

    def __init__(self, err=None, message=""):
        self.message = message
        self.err = err
        super().__init__(self.message)

        logging.error(f"{self.message} : {self.err}")

    def __str__(self):
        return self.message


class FileLoadingError(BaseCustomException):
    pass


class DistanceCalculationError(BaseCustomException):
    pass


class AutoDetectionError(BaseCustomException):
    pass

