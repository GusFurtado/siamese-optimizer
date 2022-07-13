from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
import random
from typing import Union



class Distribution(ABC):
    @abstractmethod
    def generate(self):
        pass



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



def _create_dist(dist:Union[Distribution, Number]) -> Distribution:
    if isinstance(dist, Number):
        return Constant(dist)
    return dist
