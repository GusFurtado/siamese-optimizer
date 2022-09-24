"""The submodule that defines the `Buffer` object.

`Buffer` is a model object that stores entities in-between machines.

Feed a `Line` object with this object.

"""

from dataclasses import dataclass

import simpy

from .base import Model



@dataclass
class Buffer(Model):
    """An objects that stores entities in-between machines.

    Parameters
    ----------
    name : str
        A distinct name for this object.
    capacity : int
        Maximum number of entities that can be stored in this object.
    
    """

    name : str
    capacity : int

    def _before_run(self, env:simpy.Environment, _):
        self.env = env
        self._buffer = simpy.Store(env, self.capacity)

    def _after_run(self):
        pass

    @property
    def content(self):
        return len(self._buffer.items)
