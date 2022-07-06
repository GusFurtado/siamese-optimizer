from dataclasses import dataclass

import simpy



@dataclass
class Buffer:
    name : str
    capacity : int



class _Buffer:

    def __init__(self, env:simpy.Environment, buffer:Buffer, _):
        self.env = env
        self.name = buffer.name
        self.buffer = simpy.Store(env, buffer.capacity)

    @property
    def content(self):
        return len(self.buffer.items)
