"""box.py

This file contains the Sequencer class for generating sequences of
waveforms.
"""

import typing as t
import logging
from .freqs import BaseMF
from .wave import SineWave
from .backends import BlueboxBackend, PyAudioBackend


class Sequencer:
    """Sequencer class for generating sequences of waveforms."""

    _mf: BaseMF
    _wave: SineWave
    _length: float
    _pause: float
    _sr: float
    _ch: int
    _amplitude: float
    _stop_on_error: bool
    _logger: logging.Logger
    _backend: BlueboxBackend

    def __init__(
                self,
                mf: BaseMF,
                amplitude: float = 1.0,
                length: float = 22.0,
                pause: float = 40.0,
                sample_rate: float = 44100.0,
                channels: int = 1,
                stop_on_error: bool = False,
                logger: t.Optional[logging.Logger] = None,
                backend: t.Optional[BlueboxBackend] = None) -> None:
        """Initialize the Sequencer object.

        Args:
            mf: The MF to use e.g. DTMF.
            amplitude: The combined amplitude of the waveforms.
                       The frequencies will be combined and scaled
                       to fit within this amplitude.
            length: The length of each tone in milliseconds.
            pause: The length of the pause between tones in
                     milliseconds.
            sample_rate: The sample rate of the waveforms.
            channels: The number of channels in the waveforms.
            stop_on_error: Whether to stop on an error or not.
                           If False, the error will be logged, otherwise
                            it will be raised.
        """

        self._mf = mf
        self._wave = SineWave(sr=sample_rate, ch=channels)
        self._length = length
        self._amplitude = amplitude
        self._pause = pause
        self._sr = sample_rate
        self._ch = channels
        self._stop_on_error = stop_on_error
        self._logger = logger or logging.getLogger(__name__)
        if backend is None:
            backend = PyAudioBackend(
                sample_rate=sample_rate,
                channels=channels,
                amplitude=1.0,
                logger=self._logger)
        # also check if backend is a type or an instance
        elif isinstance(backend, type):
            backend = backend(
                sample_rate=sample_rate,
                channels=channels,
                amplitude=1.0,
                logger=self._logger)
        self._backend = backend  # type: ignore        

    def sequence(self, codes: str) -> t.Iterator[float]:
        """Generate a sequence of waveforms."""
        seq_len: int = len(codes)
        i: int = 0
        for code in codes:
            try:
                freq1, freq2 = self._mf[code]
            except KeyError as e:
                if self._stop_on_error:
                    raise e
                else:
                    self._logger.error(e)
                    continue
            tone1 = self._wave.sine(
                freq1, self._length, self._amplitude / 2, 0.)
            tone2 = self._wave.sine(
                freq2, self._length, self._amplitude / 2, 0.)

            while True:
                try:
                    t1 = next(tone1)
                    t2 = next(tone2)
                    yield t1 + t2
                except StopIteration:
                    print('stop')
                    break

            i += 1
            if i < seq_len:
                pause = self._wave.sine(0., self._pause, 0., 0.)
                while True:
                    try:
                        p = next(pause)
                        yield p
                    except StopIteration:
                        break

    def __call__(self, codes: str) -> None:
        """Generate a sequence of waveforms."""
        seq = self.sequence(codes)
        self._backend.play(seq)

    def __repr__(self) -> str:
        """Get the representation of the Sequencer."""
        return f'{self.__class__.__name__}({self._mf})'
