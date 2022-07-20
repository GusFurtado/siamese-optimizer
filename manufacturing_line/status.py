from enum import Enum



class Status(Enum):
    STARVING = 1
    PROCESSING = 2
    BLOCKED = 3
    FAILURE = 4
