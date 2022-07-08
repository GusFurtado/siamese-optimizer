from dataclasses import dataclass
from numbers import Number
from typing import Union

import simpy

from manufacturing_line import distributions as dist



@dataclass
class Source:
    name : str
    creation_time : Union[dist.Distribution, Number]
    output_buffer : str



class _Source:

    def __init__(self, env:simpy.Environment, source:Source, objects:dict):
        
        # Properties
        self.name = source.name
        self.output_buffer = objects[source.output_buffer]
        self.creation_time = dist._create_spicy_dist(source.creation_time)

        # Stats
        self.items_created = 0
        self.time_blocked = 0

        # Environment
        self.env = env
        self.process = self.env.process(self.produce())


    def produce(self):
        while True:

            # Create
            yield self.env.timeout(self.creation_time.rvs())
            self.items_created += 1

            # Blocked
            blocked_start = self.env.now
            yield self.output_buffer.buffer.put(1)
            self.time_blocked += (self.env.now-blocked_start)
