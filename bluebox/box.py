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
    _pad_pause: float
    _meta_codes: t.Set[str] = set(['p', 'P'])
    _valid_codes: t.Set[str]

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
                backend: t.Optional[
                        t.Union[BlueboxBackend, t.Type[BlueboxBackend]]
                    ] = None,
                pad_pause: float = 150.0) -> None:
        """Initialize the Sequencer object.

        Args:
            mf: The MF to use e.g. DTMF.
            amplitude: The combined amplitude of the waveforms.
                       The frequencies will be combined and scaled
                       to fit within this amplitude. Must be in (0, 1.0].
            length: The length of each tone in milliseconds. Must be positive.
            pause: The length of the pause between tones in
                     milliseconds. Must be non-negative.
            sample_rate: The sample rate of the waveforms. Must be positive.
            channels: The number of channels in the waveforms.
                Must be at least 1.
            stop_on_error: Whether to stop on an error or not.
                If False, the error will be logged, otherwise
                it will be raised.
            logger: Optional logger instance for logging.
            backend: Optional backend for audio output. Can be a class
                or instance.
            pad_pause: Duration (ms) of the pause before/after sequence.
                Must be non-negative.

        Raises:
            ValueError: If any parameter is out of valid range.
        """
        # Validate parameters
        if amplitude <= 0 or amplitude > 1.0:
            raise ValueError(
                f'Amplitude must be in (0, 1.0], got {amplitude}')
        if length <= 0:
            raise ValueError(f'Length must be positive, got {length}')
        if pause < 0:
            raise ValueError(f'Pause must be non-negative, got {pause}')
        if sample_rate <= 0:
            raise ValueError(
                f'Sample rate must be positive, got {sample_rate}')
        if channels < 1:
            raise ValueError(
                f'Channels must be at least 1, got {channels}')
        if pad_pause < 0:
            raise ValueError(
                f'Pad pause must be non-negative, got {pad_pause}')

        self._mf = mf
        self._wave = SineWave(sample_rate=sample_rate, channels=channels)
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
        self._pad_pause = pad_pause

        self._valid_codes = set(
            self._mf.valid_codes() |
            self._meta_codes)

    def _pause_generator(
                        self,
                        length: t.Optional[float] = None) -> t.Iterator[float]:
        """Generate a pause waveform."""
        if length is None:
            length = self._pause
        pause = self._wave.sine(0., length, 0., 0.)
        while True:
            try:
                p = next(pause)
                yield p
            except StopIteration:
                break

    def _sine_mf_generator(
                            self,
                            freq1: float,
                            freq2: float,
                            length: t.Optional[float] = None,
                            amplitude: t.Optional[float] = None,
                            phase: float = 0.) -> t.Iterator[float]:
        """Generate a sine wave with the given frequencies."""
        if length is None:
            length = self._length
        if amplitude is None:
            amplitude = self._amplitude
        tone1 = self._wave.sine(
            freq1, length, amplitude / 2., phase)
        tone2 = self._wave.sine(
            freq2, length, amplitude / 2., phase)
        while True:
            try:
                t1 = next(tone1)
                t2 = next(tone2)
                yield t1 + t2
            except StopIteration:
                break

    def sequence(self, codes: str) -> t.Iterator[float]:
        """Generate a sequence of waveforms.

        Processes the input codes, filtering out invalid ones, and generates
        the corresponding tone sequences with proper pauses.
        """
        # Filter and validate codes first
        valid_codes = []
        for i, code in enumerate(codes):
            if code not in self._valid_codes:
                msg = (f"Invalid code '{code}' at position {i} "
                       f"in sequence '{codes}'")
                if self._stop_on_error:
                    raise ValueError(msg)
                else:
                    self._logger.warning(msg)
                    continue
            valid_codes.append(code)

        if not valid_codes:
            self._logger.info('No valid codes in sequence, nothing to play')
            return

        seq_len = len(valid_codes)

        if self._pad_pause > 0:
            # Generate a pause at the start of the sequence
            yield from self._pause_generator(self._pad_pause)

        for i, code in enumerate(valid_codes):
            if code in self._meta_codes:
                # Meta code: insert pause
                yield from self._pause_generator()
            else:
                try:
                    freq1, freq2 = self._mf[code]
                except KeyError as e:
                    if self._stop_on_error:
                        raise e
                    else:
                        self._logger.error(e)
                        continue

                yield from self._sine_mf_generator(freq1, freq2)

            # Add pause between tones (not after last tone)
            if i < seq_len - 1:
                yield from self._pause_generator()

        if self._pad_pause > 0:
            # Generate a pause at the end of the sequence
            yield from self._pause_generator(self._pad_pause)

    def __call__(self, codes: str) -> None:
        """Generate a sequence of waveforms."""
        seq = self.sequence(codes)
        self._backend.play(seq)

    def __repr__(self) -> str:
        """Get the representation of the Sequencer."""
        return f'{self.__class__.__name__}({self._mf})'
