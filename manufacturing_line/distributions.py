from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
import random
from typing import Sequence, Union



class Distribution(ABC):
    @abstractmethod
    def generate(self):
        pass



class Beta(Distribution):
    alpha : Number
    beta : Number
    max : Number = 1
    min : Number = 0

    def generate(self):
        return (self.max - self.min) \
            * random.betavariate(self.alpha, self.beta) \
            + self.min


class Choice(Distribution):
    values: Sequence[Number]

    def generate(self):
        return random.choice(self.values)



@dataclass
class Constant(Distribution):
    value: Number = 1

    def generate(self):
        return self.value



@dataclass
class Exponential(Distribution):
    mean: Number = 1
    min: Number = 0

    def generate(self):
        return random.expovariate(
            lambd = 1/(self.mean-self.min)
        ) + self.min



class Gamma(Distribution):
    alpha : Number
    beta : Number

    def generate(self):
        return random.gammavariate(self.alpha, self.beta)



@dataclass
class Normal(Distribution):
    mean: Number = 0
    std: Number = 1

    def generate(self):
        return random.normalvariate(
            mu = self.mean,
            sigma = self.std
        )



@dataclass
class Triangular(Distribution):
    min: Number = 0
    mode: Number = 0.5
    max: Number = 1

    def generate(self):
        return random.triangular(
            low = self.min,
            mode = self.mode,
            high = self.max,
        )



@dataclass
class Uniform(Distribution):
    min: Number = 0
    max: Number = 1

    def generate(self):
        return random.uniform(
            a = self.min,
            b = self.max
        )



class Weibull(Distribution):
    alpha : Number
    beta : Number

    def generate(self):
        return random.weibullvariate(self.alpha, self.beta)



def _create_dist(dist:Union[Distribution, Number]) -> Distribution:
    if isinstance(dist, Number):
        return Constant(dist)
    return dist
