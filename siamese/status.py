"""The Status class submodule."""

from enum import Enum



class Status(Enum):
    """Object that holds the status of a model.
    
    """

    STARVING = 1
    PROCESSING = 2
    BLOCKED = 3
    FAILURE = 4
