"""Submodule for base models."""

from abc import ABC, abstractmethod



class Model(ABC):
    """Abstract base class for models."""
    
    @abstractmethod
    def _before_run(self):
        """Events triggered right before simulation starts."""
        pass

    @abstractmethod
    def _after_run(self):
        """Events triggered right after simulation ends."""
        pass
