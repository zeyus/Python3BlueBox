"""backend_wav.py

This file contains the WAV file export backend for bluebox.
Allows generating WAV audio files instead of playing audio in real-time.
"""

import typing as t
import logging
import wave
import struct
from pathlib import Path
from .base import BlueboxBackend


class WavBackend(BlueboxBackend):
    """WavBackend class for exporting to WAV files."""

    _output_path: Path
    _buffer: t.List[float]

    def __init__(
                self,
                sample_rate: float = 44100.0,
                channels: int = 1,
                amplitude: float = 1.0,
                logger: t.Optional[logging.Logger] = None,
                output_path: t.Optional[t.Union[str, Path]] = None,
                **kwargs: t.Any) -> None:
        """Initialize the WAV backend.

        Args:
            sample_rate: Sample rate in Hz.
            channels: Number of audio channels (1 for mono, 2 for stereo).
            amplitude: Maximum amplitude (0.0 to 1.0).
            logger: Optional logger instance.
            output_path: Path where the WAV file will be saved (required).

        Raises:
            ValueError: If output_path is not provided.
        """
        super().__init__(sample_rate, channels, amplitude, logger,
                         output_path, **kwargs)
        if output_path is None:
            raise ValueError('WAV backend requires output_path parameter')
        self._output_path = Path(output_path)
        self._buffer = []
        # Store sample rate for WAV file writing
        self._wav_sample_rate = int(sample_rate)

    def _to_bytes(self, data: t.Iterator[float]) -> t.List[float]:
        """Convert iterator to list of floats."""
        return list(data)

    def play(self, data: t.Iterator[float], close: bool = True) -> None:
        """Buffer audio data for later export.

        Args:
            data: Iterator of audio samples as floats in range [-1.0, 1.0].
            close: If True, write the buffered data to file after buffering.
        """
        self._buffer.extend(self._to_bytes(data))
        if close:
            self.close()

    def play_all(self, queue: t.Iterator[t.Iterator[float]]) -> None:
        """Buffer all audio data and export to WAV file.

        Args:
            queue: Iterator of audio data iterators.
        """
        for data in queue:
            self.play(data, close=False)
        self.close()

    def stop(self) -> None:
        """Stop operation (no-op for WAV backend)."""
        pass

    def close(self) -> None:
        """Write buffered audio data to WAV file.

        Converts float samples [-1.0, 1.0] to 16-bit PCM and writes
        to the specified output path.
        """
        if not self._buffer:
            self._logger.warning('No audio data to write to WAV file')
            return

        try:
            with wave.open(str(self._output_path), 'wb') as wav:
                wav.setnchannels(self._ch)
                wav.setsampwidth(2)  # 16-bit audio
                wav.setframerate(self._wav_sample_rate)

                # Convert float [-1.0, 1.0] to int16 [-32768, 32767]
                samples = [
                    max(-32768, min(32767, int(s * 32767)))
                    for s in self._buffer
                ]
                wav.writeframes(struct.pack(f'{len(samples)}h', *samples))

            self._logger.info(
                f'Wrote {len(self._buffer)} samples to WAV file: '
                f'{self._output_path}')
            self._buffer.clear()

        except Exception as e:
            self._logger.error(f'Failed to write WAV file: {e}')
            raise

    def __del__(self) -> None:
        """Ensure buffered data is written on cleanup."""
        if self._buffer:
            try:
                self.close()
            except Exception:
                pass  # Already logged in close()

    def clear_buffer(self) -> None:
        """Clear the audio buffer without writing to file."""
        self._buffer.clear()
