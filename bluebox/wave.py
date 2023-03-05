"""wave.py

This file contains the Wave class for generating waveforms.
It is completely generic and backend agnostic, but does not
provide any functionality for playing the waveforms. That is
handled in the backend specific files.
"""

import typing as t
import math
from array import array


class SineWave:
    """SineWave class for generating waveform arrays."""

    _sample_rate: float = 44100.0
    _channels: int = 1

    def __init__(
                self,
                sr: t.Optional[float] = None,
                ch: t.Optional[int] = None) -> None:
        """Initialize the Wave object."""
        if sr is not None:
            self._sample_rate = sr
        if ch is not None:
            self._channels = ch

    def sine(
            self,
            freq: float,
            length: float,
            amplitude: float = 1.0,
            phase: float = 0.0) -> t.MutableSequence[float]:
        """Generate a sine wave.

        Args:
            freq: The frequency of the sine wave.
            length: The length of the sine wave in seconds.
            amplitude: The amplitude of the sine wave.
            phase: The phase of the sine wave.


        Returns:
            An array representing the sine wave.
        """
        wave = array('f')

        # silence / pauses
        if freq == 0.0 or amplitude == 0.0:
            for i in range(math.ceil(length * self._sample_rate)):
                wave.append(0.0)
            return wave

        # sine wave
        for i in range(math.ceil(length * self._sample_rate)):
            wave.append(
                amplitude * math.sin(
                    2 * math.pi * freq * (i / self._sample_rate) + phase))
        return wave

    def __call__(
                self,
                freq: float,
                length: float,
                amplitude: float = 1.0,
                phase: float = 0.0) -> t.MutableSequence[float]:
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
        return f'{self.__class__.__name__}(Sample Rate: {self._sample_rate}, Channels: {self._channels})'  # noqa: E501
