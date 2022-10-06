from .logger import logging


class FileLoadingError(Exception):

    def __init__(self, err, message=""):
        self.message = message
        self.err = err
        super().__init__(self.message)

        logging.error(f"{self.message} : {self.err}")

    def __str__(self):
        return self.message
