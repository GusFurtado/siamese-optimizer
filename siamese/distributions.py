"""Submodule for statistical distribution objects."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
import random
from typing import Sequence, Union



class Distribution(ABC):
    """Abstract base class for distributions."""

    @abstractmethod
    def generate(self):
        """Generates a value based on the subclass distribution."""
        pass



class Beta(Distribution):
    """Generate a value based on a beta distribution.

    The beta distribution is a family of continuous probability distributions
    parameterized by two positive shape parameters (`alpha` and `beta`).

    The original distribution is defined on the interval between 0 and 1, but
    it is possible to scale the shape with the `min` and `max` parameters.

    Parameters
    ----------
    alpha : Number
        First shape parameter.
    beta : Number
        Second shape parameter.
    max : Number, default=1
        The biggest possible number to be generated.
    min : Number, default=0
        The smallest possible number to be generated.
    
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Beta_distribution

    """

    alpha : Number
    beta : Number
    max : Number = 1
    min : Number = 0

    def __post_init__(self):
        if (self.alpha <= 0) or (self.beta <= 0):
            raise ValueError(
                'Both `alpha` and `beta` parameters must be positive numbers.'
            )
        if self.min >= self.max:
            raise ValueError(
                'The `max` parameter must be bigger then `min`.'
            )

    def generate(self):
        return (self.max - self.min) \
            * random.betavariate(self.alpha, self.beta) \
            + self.min


class Choice(Distribution):
    """Randomly picks a value from a list of values.

    Parameters
    ----------
    values : Squence[Number]
        A sequence of numbers.
    
    """

    values: Sequence[Number]

    def generate(self):
        return random.choice(self.values)



@dataclass
class Constant(Distribution):
    """Always generate the same value.

    Parameters
    ----------
    value : Number, default=1
        Constant value to be generated.
    
    """

    value: Number = 1

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(
                '`value` must be bigger than zero.'
            )

    def generate(self):
        return self.value



@dataclass
class Exponential(Distribution):
    """Generate a value based on an exponential distribution.

    Parameters
    ----------
    mean : Number, default=1
        Expected mean value to be generated.
    min : Number, default=0
        The smallest possible number to be generated.
    
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Exponential_distribution
    
    """

    mean: Number = 1
    min: Number = 0

    def __post_init__(self):
        if self.min >= self.mean:
            raise ValueError(
                'The `mean` parameter must be bigger than `min`.'
            )
        if self.min < 0:
            raise ValueError(
                'The `min` parameter must be equal or bigger than zero.'
            )

    def generate(self):
        return random.expovariate(
            lambd = 1/(self.mean-self.min)
        ) + self.min



class Gamma(Distribution):
    """Generate a value based on a gamma distribution.

    The gamma distribution is a two-parameter family of continuous probability
    distributions.
    
    Both shape and scale parameters must be positive real numbers.

    Parameters
    ----------
    shape : Number
        The shape parameter, also known as "k" or "alpha".
    scale : Number
        The scale parameter, also known as "theta" or "beta".

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Gamma_distribution

    """

    shape : Number
    scale : Number

    def __post__init__(self):
        if (self.shape <= 0) or (self.scale <= 0):
            raise ValueError(
                'Both `shape` and `scale` parameters must be positive numbers.'
            )

    def generate(self):
        return random.gammavariate(self.shape, self.scale)



@dataclass
class Normal(Distribution):
    """Generate a value based on a normal distribution.
    
    Parameters
    ----------
    mean : Number, default=0
        Expected mean value, also known as "mu".
    std : Number, default=1
        Standard deviation, also known as "sigma".

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Normal_distribution

    """

    mean: Number = 0
    std: Number = 1

    def __post_init__(self):
        if self.std <= 0:
            raise ValueError(
                'The `std` parameter must be bigger then zero.'
            )

    def generate(self):
        return random.normalvariate(
            mu = self.mean,
            sigma = self.std
        )



@dataclass
class Triangular(Distribution):
    """Generate a value based on a triangular distribution.
    
    The triangular distribution is a continuous probability distribution with
    lower limit `min`, upper limit `max` and `mode`, where `min` < `max` and
    `min` ≤ `mode` ≤ `max`.

    Parameters
    ----------
    max : Number, default=1
        The biggest possible number to be generated.
    mode : Number, default=0.5
        The point of the distribution with higher frequency of occurrence.
    min : Number, default=0
        The smallest possible number to be generated.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Triangular_distribution

    """

    min: Number = 0
    mode: Number = 0.5
    max: Number = 1

    def __post_init__(self):
        if self.min > self.mode:
            raise ValueError(
                'The `mode` parameter must be equal or bigger then `min`.'
            )
        if self.mode > self.max:
            raise ValueError(
                'The `max` parameter must be equal or bigger then `mode`.'
            )
        if self.min >= self.max:
            raise ValueError(
                'The `max` parameter must be bigger then `min`.'
            )

    def generate(self):
        return random.triangular(
            low = self.min,
            mode = self.mode,
            high = self.max,
        )



@dataclass
class Uniform(Distribution):
    """Generate a value based on a continuous uniform distribution.
    
    The continuous uniform distribution or rectangular distribution is a
    family of symmetric probability distributions that describes an experiment
    where there is an arbitrary outcome that lies between certain bounds where
    all intervals of the same length are equally probable.

    Parameters
    ----------
    max : Number, default=1
        The biggest possible number to be generated.
    min : Number, default=0
        The smallest possible number to be generated.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Continuous_uniform_distribution

    """

    min: Number = 0
    max: Number = 1

    def generate(self):
        return random.uniform(
            a = self.min,
            b = self.max
        )



class Weibull(Distribution):
    """Generate a value based on a Weibull distribution.

    The Weibull distribution is a two-parameter family of continuous
    probability distributions.
    
    Both shape and scale parameters must be positive real numbers.

    Parameters
    ----------
    shape : Number
        The shape parameter, also known as "lambda" or "alpha".
    scale : Number
        The scale parameter, also known as "k" or "beta".

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Weibull_distribution

    """

    shape : Number
    scale : Number

    def __post__init__(self):
        if (self.shape <= 0) or (self.scale <= 0):
            raise ValueError(
                'Both `shape` and `scale` parameters must be positive numbers.'
            )

    def generate(self):
        return random.weibullvariate(self.scale, self.shape)



def _create_dist(dist:Union[Distribution, Number]) -> Distribution:
    if isinstance(dist, Number):
        return Constant(dist)
    return dist
