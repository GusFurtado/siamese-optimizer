"""Submodule for base models."""

from abc import ABC, abstractmethod



class Model(ABC):
    """Base model type."""
    
    @abstractmethod
    def _before_run(self):
        pass

    @abstractmethod
    def _after_run(self):
        pass
