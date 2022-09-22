"""The Failure objects submodule.

A `Failure` object holds the parameters of a model failure behavior through
its `failure` argument.

This behavior is defined by how long it takes for a machine to break (change
to its failure state) and how long it takes to return to its original working
state.

"""

from dataclasses import dataclass
from numbers import Number
from typing import Union

from siamese.distributions import Distribution



class Failure:
    """Base Failure type."""
    pass



@dataclass
class CountFailure(Failure):
    """A item count-based failure model.
    
    Parameters
    ----------
    items_between_failures : Distribution | Number
        How many items need to be processed to change the model status from
        `PROCESSING` to `FAILURE`.
    time_to_repair : Distribution | Number
        How many failure time is necessary to change the model status from
        `FAILURE` back to `PROCESSING`.

    """

    items_between_failures : Union[Distribution, Number]
    time_to_repair : Union[Distribution, Number]



@dataclass
class TimeFailure(Failure):
    """A time-based failure model.
    
    Parameters
    ----------
    time_between_failures : Distribution | Number
        How many processing time is necessary to change the model status from
        `PROCESSING` to `FAILURE`.
    time_to_repair : Distribution | Number
        How many failure time is necessary to change the model status from
        `FAILURE` back to `PROCESSING`.

    """

    time_between_failures : Union[Distribution, Number]
    time_to_repair : Union[Distribution, Number]
