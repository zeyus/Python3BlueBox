"""box.py

This file contains the Sequencer class for generating sequences of
waveforms.
"""

import typing as t
import logging
from array import array
from .freqs import BaseMF
from .wave import SineWave


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

    def __init__(
                self,
                mf: BaseMF,
                amplitude: float = 1.0,
                length: float = 22.0,
                pause: float = 40.0,
                sample_rate: float = 44100.0,
                channels: int = 1,
                stop_on_error: bool = False,
                logger: t.Optional[logging.Logger] = None) -> None:
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
        self.amplitude = amplitude
        self._pause = pause
        self._sr = sample_rate
        self._ch = channels
        self._stop_on_error = stop_on_error
        self._logger = logger or logging.getLogger(__name__)

    def sequence(self, codes: str) -> t.Iterator[t.MutableSequence[float]]:
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
            tone1 = self._wave.sine(freq1, self._length, self._amplitude, 0.)
            tone2 = self._wave.sine(freq2, self._length, self._amplitude, 0.)
            mftone = array(
                'f',
                [tone1[i] + tone2[i] for i in range(len(tone1))])
            pause = self._wave.sine(0., self._pause, 0., 0.)
            i += 1
            yield mftone
            # no pause if last
            if i < seq_len:
                yield pause
        raise StopIteration

    def __call__(self, codes: str) -> t.Iterator[t.MutableSequence[float]]:
        """Generate a sequence of waveforms."""
        return self.sequence(codes)

    def __repr__(self) -> str:
        """Get the representation of the Sequencer."""
        return f'{self.__class__.__name__}({self._mf})'
