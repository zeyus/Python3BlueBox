"""base.py

This file contains the base class for the backends.
"""

from abc import ABC, abstractmethod
import typing as t
import logging


class BlueboxBackend(ABC):
    """BlueboxBackend class for defining backends."""

    _sr: float = 44100.0
    _ch: int = 1
    _amplitude: float = 1.0
    _logger: logging.Logger

    def __init__(
                self,
                sample_rate: float = 44100.0,
                channels: int = 1,
                amplitude: float = 1.0,
                logger: t.Optional[logging.Logger] = None) -> None:
        """Initialize the backend."""
        self._sr = sample_rate
        self._ch = channels
        self._amplitude = amplitude
        self._logger = logger or logging.getLogger(__name__)

    @abstractmethod
    def play(self, data: t.Iterator[float]) -> None:
        """Play the given data."""

    @abstractmethod
    def play_all(self, queue: t.Iterator[t.Iterator[float]]) -> None:
        """Play the given data and then stop."""

    @abstractmethod
    def stop(self) -> None:
        """Stop playing the data."""

    @abstractmethod
    def close(self) -> None:
        """Close the backend."""

    @abstractmethod
    def __del__(self) -> None:
        """Delete the backend."""
        self.close()
