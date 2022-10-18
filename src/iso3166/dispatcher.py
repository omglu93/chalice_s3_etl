import pandas as pd
from typing import Callable


class DynamicFileReadingDispatcher(object):

    """
    Class creates a dispatcher that allows the user to register other
    functions via wrapper. The function is registered with a string that
    acts as the variable (key) in a dictionary.
    """

    def __init__(self, state_attr='state'):
        self.registry = {}
        self._state_attr = state_attr

    def __get__(self, instance, owner):
        if instance is None:
            return self

        method = self.registry[getattr(instance, self._state_attr)]
        return method.__get__(instance, owner)

    def register(self, state):

        """
        ## **Function**
        ----------

        The function registers another function and adds it to a dictionary
        based on the state. For example: dict[state] = function.

        ## **Parameters**
        ----------
        `state`:
            The string used to identify the function.

        `return None`
        """

        def decorator(method):
            self.registry[state] = method
            return method

        return decorator


class DynamicFileMachine(object):

    """
    Class is used to register custom read functions and add them to the
    dictionary. Extensions to the functionality or other custom functions
    can be added into this class by using a @dispatcher.register decorator.
    """

    def __init__(self, state):
        self.state = state

    dispatcher = DynamicFileReadingDispatcher()

    @dispatcher.register(".csv")
    def _custom_read_csv(self) -> Callable:
        return pd.read_csv

    @dispatcher.register(".json")
    def _custom_read_json(self) -> Callable:
        return pd.read_json

    @dispatcher.register(".parquet")
    def _custom_read_parquet(self) -> Callable:
        return pd.read_parquet

    @dispatcher.register(".txt")
    def _custom_read_text(self) -> Callable:
        return pd.read_fwf
