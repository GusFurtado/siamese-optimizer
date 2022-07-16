from dataclasses import dataclass
from numbers import Number
from typing import Optional, Union

import simpy

from manufacturing_line import distributions as dist
from manufacturing_line import failures as fail
from manufacturing_line._reports import SourceReport
from .base import Model



@dataclass
class Source(Model):
    name : str
    creation_time : Union[dist.Distribution, Number]
    output_buffer : str
    failure : Optional[fail.Failure] = None


    def _before_run_starts(self, env:simpy.Environment, objects:dict):
        
        # Properties
        self.output_buffer = objects[self.output_buffer]
        self.creation_time = dist._create_dist(self.creation_time)

        # Stats
        self.items_created = 0
        self.time_blocked = 0
        self.time_broken = 0
        self.time_creating = 0

        # Environment
        self.env = env
        self.process = self.env.process(self._run_process())

        # Failure
        if isinstance(self.failure, fail.Failure):
            self.tbf = dist._create_dist(self.failure.time_between_failures)
            self.ttr = dist._create_dist(self.failure.time_to_repair)
            self.reset_on_failure = self.failure.reset_process
            env.process(self._run_failure())


    def _run_process(self):

        part = None
        while True:
            
            # Creating
            creation_time = self.creation_time.generate()
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
                    yield self.env.timeout(self.ttr.generate())
                    self.time_broken += (self.env.now-failure_start)

            # Blocked
            while part:
                try:
                    blocked_start = self.env.now
                    yield self.output_buffer._buffer.put(part)
                    part = None
                    self.time_blocked += (self.env.now-blocked_start)
                except simpy.Interrupt:
                    self.time_blocked += (self.env.now-blocked_start)
                    failure_start = self.env.now
                    yield self.env.timeout(self.ttr.generate())
                    self.time_broken += (self.env.now-failure_start)


    def _run_failure(self):
        while True:
            yield self.env.timeout(self.tbf.generate())
            self.process.interrupt()


    def _after_run_ends(self):
        try:
            self.average_creation_time = self.time_creating / self.items_created
        except ZeroDivisionError:
            self.average_creation_time = 0


    @property
    def report(self) -> str:
        return SourceReport(self)
