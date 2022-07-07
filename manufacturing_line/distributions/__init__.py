from dataclasses import dataclass
from scipy import stats



@dataclass
class Exponential:
    mean: float = 1
    min: float = 0



@dataclass
class Normal:
    mean: float = 0
    std: float = 1



@dataclass
class Triangular:
    min: float = 0
    mode: float = 0.5
    max: float = 1



@dataclass
class Uniform:
    min: float = 0
    max: float = 1



def _get_scipy_distribution(dist):

    if isinstance(dist, Exponential):
        return stats.expon(
            loc = dist.min,
            scale = dist.mean - dist.min
        )

    elif isinstance(dist, Normal):
        return stats.norm(
            loc = dist.mean,
            scale = dist.std    
        )

    elif isinstance(dist, Triangular):
        return stats.triang(
            loc = dist.min,
            scale = dist.max - dist.min,
            c = (dist.mode-dist.min) / (dist.max-dist.min)
        )

    elif isinstance(dist, Uniform):
        return stats.uniform(
            loc = dist.min,
            scale = dist.max - dist.min
        )
