from dataclasses import dataclass
from numbers import Number
from typing import Union

from manufacturing_line.distributions import Distribution



class Failure:
    pass



@dataclass
class CountFailure(Failure):
    items_between_failures : Union[Distribution, Number]
    time_to_repair : Union[Distribution, Number]



@dataclass
class TimeFailure(Failure):
    time_between_failures : Union[Distribution, Number]
    time_to_repair : Union[Distribution, Number]
    reset_process : bool = False
