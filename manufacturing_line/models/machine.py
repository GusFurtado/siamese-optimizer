from dataclasses import dataclass
from numbers import Number
from typing import Union

import simpy

from manufacturing_line import distributions as dist



@dataclass
class Machine:
    name : str
    processing_time : Union[dist.Distribution, Number]
    input_buffer : str
    output_buffer : str



class _Machine:

    def __init__(self, env:simpy.Environment, machine:Machine, objects:dict):
        
        # Properties
        self.name = machine.name
        self.input_buffer = objects[machine.input_buffer]
        self.output_buffer = objects[machine.output_buffer]
        self.processing_time = dist._create_spicy_dist(machine.processing_time)

        # Stats
        self.time_starved = 0
        self.time_processing = 0
        self.time_blocked = 0
        self.items_processed = 0
        
        # Environment
        self.env = env
        self.process = self.env.process(self.produce())


    def produce(self):
        while True:

            # Starving
            starving_start = self.env.now
            part = yield self.input_buffer.buffer.get()
            processing_start = self.env.now
            self.time_starved += (processing_start-starving_start)

            # Processing
            yield self.env.timeout(self.processing_time.rvs())
            blocked_start = self.env.now
            self.items_processed += 1
            self.time_processing += (blocked_start-processing_start)

            # Blocked
            yield self.output_buffer.buffer.put(part)
            self.time_blocked += (self.env.now-blocked_start)
