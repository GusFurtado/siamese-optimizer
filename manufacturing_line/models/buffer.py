from dataclasses import dataclass

import simpy

from .base import Model



@dataclass
class Buffer(Model):
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
