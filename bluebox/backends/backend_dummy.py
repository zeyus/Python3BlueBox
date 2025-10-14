"""backend_dummy.py

This file contains the dummy backend for bluebox.
This is used for testing and instead of generating
sound, it can print the data to the console, or return
it as a list.
"""

import typing as t
import logging
from .base import BlueboxBackend


class DummyBackend(BlueboxBackend):
    """DummyBackend class for the dummy backend."""

    _data: t.List[float]

    def __init__(
                self,
                sample_rate: float = 44100.0,
                channels: int = 1,
                amplitude: float = 1.0,
                logger: t.Optional[logging.Logger] = None,
                mode: str = 'print',
                **kwargs: t.Any) -> None:
        """Initialize the dummy backend."""
        super().__init__(sample_rate, channels, amplitude, logger, **kwargs)
        self._mode = mode
        self._data = []

    def _to_bytes(self, data: t.Iterator[float]) -> t.List[float]:
        """Wrap the data in a buffer."""
        _data = []
        while True:
            try:
                d = next(data)
                _data.append(d)
            except StopIteration:
                break

        return _data

    def play(self, data: t.Iterator[float], close: bool = True) -> None:
        """Play the given data."""
        d = self._to_bytes(data)
        if self._mode == 'print':
            print(d)
        elif self._mode == 'list':
            self._data += d
        else:
            raise ValueError(f'Invalid mode: {self._mode}')

    def play_all(self, queue: t.Iterator[t.Iterator[float]]) -> None:
        """Play the given data and then stop."""
        for data in queue:
            self.play(data, close=False)

    def stop(self) -> None:
        """Stop playing the data."""
        pass

    def close(self) -> None:
        """Close the backend."""
        pass

    def __del__(self) -> None:
        """Delete the backend."""
        self.close()

    def get_data(self) -> t.List[float]:
        """Get the data."""
        return self._data

    def clear_data(self) -> None:
        """Clear the data."""
        self._data = []
