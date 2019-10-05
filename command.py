from collections import namedtuple
from typing import List

ExecutionResult = namedtuple("ExecutionResult", ["type", "payload"])
ExecutionResult.__new__.__defaults__ = (None,) * len(ExecutionResult._fields)

REGISTRY = {}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Command(metaclass=Singleton):
    """
    The normal API browser command. The fields are used in form_builder to render the form on canvas
    And allows hook to execute the command on input
    """

    def title(self) -> str:
        raise NotImplementedError

    def form_fields(self) -> List[dict]:
        raise NotImplementedError

    def description(self) -> str:
        return self.title()

    def execute(self, params: dict) -> ExecutionResult:
        raise NotImplementedError


def register(command_type):
    """ A Decorator that helps to register command

    # Arguments

        command_type: string to store the command
        :return: the wrapped
    """

    def wrapper(singleton):
        REGISTRY[command_type] = singleton()
        return singleton

    return wrapper


def registered_commands():
    return REGISTRY
