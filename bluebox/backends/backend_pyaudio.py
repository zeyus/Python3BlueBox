"""backend_pyaudio.py

This file contains the PyAudio backend for bluebox.
"""

import typing as t
import logging
import struct
import pyaudio
from .base import BlueboxBackend


class PyAudioBackend(BlueboxBackend):
    """PyAudioBackend class for the PyAudio backend."""

    _stream: pyaudio.Stream
    _stream_open: bool = False
    _device: t.Union[int, None]

    def __init__(
                self,
                sample_rate: float = 44100.0,
                channels: int = 1,
                amplitude: float = 1.0,
                logger: t.Optional[logging.Logger] = None,
                device: t.Union[int, None] = None) -> None:
        """Initialize the PyAudio backend."""
        super().__init__(sample_rate, channels, amplitude, logger)
        self._device = device

    def _get_stream(self) -> pyaudio.Stream:
        """Get the PyAudio stream."""
        if not self._stream_open:
            self._stream = pyaudio.PyAudio().open(
                format=pyaudio.paFloat32,
                channels=self._ch,
                rate=int(self._sr),
                output=True,
                output_device_index=self._device)
            self._stream_open = True
        return self._stream

    def _to_bytes(self, data: t.Iterator[float]) -> bytes:
        """Wrap the data in a buffer."""
        _data = []
        while True:
            try:
                d = next(data)
                _data.append(d)
            except StopIteration:
                break

        return struct.pack(f'{len(_data)}f', *_data)

    def play(self, data: t.Iterator[float], close=True) -> None:
        """Play the given data."""
        d = self._to_bytes(data)
        self._get_stream().write(d)
        if close:
            self.close()

    def play_all(self, queue: t.Iterator[t.Iterator[float]]) -> None:
        """Play all the items until the end."""
        while True:
            try:
                data = next(queue)
                self.play(data, False)
            except StopIteration:
                break
        self.close()

    def stop(self) -> None:
        """Stop playing the data."""
        if self._stream_open:
            self._stream.stop_stream()

    def close(self) -> None:
        """Close the backend."""
        if self._stream_open:
            self._stream.close()
            self._stream_open = False

    def __del__(self) -> None:
        """Close the backend."""
        self.close()


class PyAudioBackendNonBlocking(PyAudioBackend):
    """PyAudioBackendNonBlocking class for the PyAudio backend."""

    def _get_stream(self, callback: t.Callable) -> pyaudio.Stream:
        """Get the PyAudio stream."""
        if not self._stream_open:
            self._stream = pyaudio.PyAudio().open(
                format=pyaudio.paFloat32,
                channels=self._ch,
                rate=int(self._sr),
                output=True,
                stream_callback=callback,
                output_device_index=self._device)
            self._stream_open = True
        return self._stream

    @property
    def is_playing(self) -> bool:
        """Return whether the stream is playing."""
        if not self._stream_open:
            return False
        return self._stream.is_active()

    def play(self, data: t.MutableSequence[float]) -> None:
        """Play the given data."""
        total_frames = len(data)
        frame_index = 0

        def stream_callback(
                            in_data: t.Optional[t.MutableSequence[bytes]],
                            frame_count: int,
                            time_info: t.Optional[dict],
                            status: t.Optional[int]) -> t.Tuple[
                                t.Optional[t.MutableSequence[float]],
                                int]:
            nonlocal frame_index
            if frame_index >= total_frames:
                return (None, pyaudio.paComplete)
            frame_index += min(frame_count, total_frames - frame_index)
            return (
                data[frame_index - frame_count:frame_index],
                pyaudio.paContinue)

        self._get_stream(stream_callback)

    def play_all(self, queue: t.Iterator[t.MutableSequence[float]]) -> None:
        """Not implemented. Probably should use asyncio."""
        raise NotImplementedError()
