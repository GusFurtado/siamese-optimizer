from dataclasses import dataclass
from numbers import Number
from typing import Optional, Union

import simpy

from manufacturing_line import distributions as dist
from manufacturing_line import failures as fail
from manufacturing_line._reports import MachineReport
from .base import Model



@dataclass
class Machine(Model):
    name : str
    processing_time : Union[dist.Distribution, Number]
    input_buffer : str
    output_buffer : str
    failure : Optional[fail.Failure] = None


    def _before_run_starts(self, env:simpy.Environment, objects:dict):
        
        # Properties
        self.input_buffer = objects[self.input_buffer]
        self.output_buffer = objects[self.output_buffer]
        self.processing_time = dist._create_dist(self.processing_time)

        # Stats
        self.time_starved = 0
        self.time_processing = 0
        self.time_blocked = 0
        self.time_broken = 0
        self.items_processed = 0
        
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

            # Starving
            while not part:
                try:
                    starving_start = self.env.now
                    part = yield self.input_buffer._buffer.get()
                    self.time_starved += (self.env.now-starving_start)
                except simpy.Interrupt:
                    self.time_starved += (self.env.now-starving_start)
                    failure_start = self.env.now
                    yield self.env.timeout(self.ttr.generate())
                    self.time_broken += (self.env.now-failure_start)

            # Processing
            processing_time = self.processing_time.generate()
            while processing_time:
                try:
                    processing_start = self.env.now
                    yield self.env.timeout(processing_time)
                    self.items_processed += 1
                    self.time_processing += (self.env.now-processing_start)
                    processing_time = 0
                except simpy.Interrupt:
                    self.time_processing += (self.env.now-processing_start)
                    if not self.reset_on_failure:
                        processing_time -= (self.env.now-processing_start)
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
            self.average_processing_time = self.time_processing / self.items_processed
        except ZeroDivisionError:
            self.average_processing_time = 0


    @property
    def report(self) -> str:
        return MachineReport(self)
