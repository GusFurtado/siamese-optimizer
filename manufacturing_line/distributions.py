from abc import ABC, abstractmethod
from dataclasses import dataclass
from numbers import Number
from typing import Union

import numpy as np
from scipy import stats



class Distribution(ABC):
    @abstractmethod
    def _scipy_dist(self):
        pass



@dataclass
class Constant(Distribution):
    value: Number = 1

    def _scipy_dist(self):
        return self

    def rvs(self, size:int=1):
        if size > 1:
            return np.repeat(self.value, repeats=size)
        return self.value



@dataclass
class Exponential(Distribution):
    mean: Number = 1
    min: Number = 0

    def _scipy_dist(self):
        return stats.expon(
            loc = self.min,
            scale = self.mean - self.min
        )



@dataclass
class Normal(Distribution):
    mean: Number = 0
    std: Number = 1

    def _scipy_dist(self):
        return stats.norm(
            loc = self.mean,
            scale = self.std    
        )



@dataclass
class Triangular(Distribution):
    min: Number = 0
    mode: Number = 0.5
    max: Number = 1

    def _scipy_dist(self):
        return stats.triang(
            loc = self.min,
            scale = self.max - self.min,
            c = (self.mode-self.min) / (self.max-self.min)
        )



@dataclass
class Uniform(Distribution):
    min: Number = 0
    max: Number = 1

    def _scipy_dist(self):
        return stats.uniform(
            loc = self.min,
            scale = self.max - self.min
        )



def _create_spicy_dist(dist:Union[Distribution, Number]):
    if isinstance(dist, Number):
        dist = Constant(dist)
    return dist._scipy_dist()
