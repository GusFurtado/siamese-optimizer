from dataclasses import dataclass
from numbers import Number
from typing import Optional, Union

import simpy

from manufacturing_line import distributions as dist
from manufacturing_line import failures as fail
from manufacturing_line._reports import SourceReport
from .base import Equipment



@dataclass
class Source(Equipment):
    name : str
    creation_time : Union[dist.Distribution, Number]
    output_buffer : str
    failure : Optional[fail.Failure] = None

    @property
    def _model_type(self):
        return _Source



class _Source(Equipment):

    def __init__(self, env:simpy.Environment, source:Source, objects:dict):
        
        # Properties
        self.name = source.name
        self.output_buffer = objects[source.output_buffer]
        self.creation_time = dist._create_spicy_dist(source.creation_time)

        # Stats
        self.items_created = 0
        self.time_blocked = 0
        self.time_broken = 0
        self.time_creating = 0

        # Environment
        self.env = env
        self.process = self.env.process(self.produce())

        # Failure
        if isinstance(source.failure, fail.Failure):
            self.tbf = dist._create_spicy_dist(source.failure.time_between_failures)
            self.ttr = dist._create_spicy_dist(source.failure.time_to_repair)
            self.reset_on_failure = source.failure.reset_process
            env.process(self.process_failure())


    def produce(self):

        part = None
        while True:
            
            # Creating
            creation_time = self.creation_time.rvs()
            while not part:
                try:
                    creation_start = self.env.now
                    yield self.env.timeout(creation_time)
                    part = 1
                    self.items_created += 1
                    self.time_creating += (self.env.now-creation_start)
                except simpy.Interrupt:
                    self.time_creating += (self.env.now-creation_start)
                    if not self.reset_on_failure:
                        creation_time -= (self.env.now-creation_start)
                    failure_start = self.env.now
                    yield self.env.timeout(self.ttr.rvs())
                    self.time_broken += (self.env.now-failure_start)

            # Blocked
            while part:
                try:
                    blocked_start = self.env.now
                    yield self.output_buffer.buffer.put(part)
                    part = None
                    self.time_blocked += (self.env.now-blocked_start)
                except simpy.Interrupt:
                    self.time_blocked += (self.env.now-blocked_start)
                    failure_start = self.env.now
                    yield self.env.timeout(self.ttr.rvs())
                    self.time_broken += (self.env.now-failure_start)


    def process_failure(self):
        while True:
            yield self.env.timeout(self.tbf.rvs())
            self.process.interrupt()


    @property
    def report(self) -> str:
        return SourceReport(self)
