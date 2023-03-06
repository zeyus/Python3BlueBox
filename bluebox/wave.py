"""wave.py

This file contains the Wave class for generating waveforms.
It is completely generic and backend agnostic, but does not
provide any functionality for playing the waveforms. That is
handled in the backend specific files.
"""

import typing as t
import math


class SineWave:
    """SineWave class for generating waveform arrays."""

    _sr: float = 44100.0
    _ch: int = 1

    def __init__(
                self,
                sample_rate: t.Optional[float] = None,
                channels: t.Optional[int] = None) -> None:
        """Initialize the Wave object."""
        if sample_rate is not None:
            self._sr = sample_rate
        if channels is not None:
            self._ch = channels

    def sine(
            self,
            freq: float,
            length: float,
            amplitude: float = 1.0,
            phase: float = 0.0) -> t.Iterator[float]:
        """Generate a sine wave.

        Args:
            freq: The frequency of the sine wave.
            length: The length of the sine wave in milliseconds.
            amplitude: The amplitude of the sine wave.
            phase: The phase of the sine wave.


        Returns:
            An array representing the sine wave.
        """

        # silence / pauses
        if freq == 0.0 or amplitude == 0.0:
            for i in range(math.ceil(length * self._sr / 1000)):
                yield 0.0
            return

        # sine wave
        for i in range(math.ceil(length * self._sr / 1000)):
            yield amplitude * math.sin(
                    2 * math.pi * freq * (i / self._sr) + phase)

    def __call__(
                self,
                freq: float,
                length: float,
                amplitude: float = 1.0,
                phase: float = 0.0) -> t.Iterator[float]:
        """Generate a sine wave.

        Args:
            freq: The frequency of the sine wave.
            length: The length of the sine wave in seconds.
            amplitude: The amplitude of the sine wave.
            phase: The phase of the sine wave.

        Returns:
            An array representing the sine wave.
        """
        return self.sine(
            freq,
            length,
            amplitude,
            phase)

    def __repr__(self) -> str:
        """Get the representation of the Wave."""
        return f'{self.__class__.__name__}(Sample Rate: {self._sr}, Channels: {self._ch})'  # noqa: E501
