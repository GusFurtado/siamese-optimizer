from dataclasses import dataclass

import simpy

from .model import Model



@dataclass
class Buffer(Model):
    name : str
    capacity : int

    def _model_type(self):
        return _Buffer



class _Buffer(Model):

    def __init__(self, env:simpy.Environment, buffer:Buffer, _):
        self.env = env
        self.name = buffer.name
        self.buffer = simpy.Store(env, buffer.capacity)

    @property
    def content(self):
        return len(self.buffer.items)
