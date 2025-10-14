"""test_wav.py

Tests for the WAV backend.
"""

import unittest
import tempfile
import wave
from pathlib import Path
from bluebox.backends.backend_wav import WavBackend
from bluebox.box import Sequencer
from bluebox.freqs import DTMF


class TestWavBackend(unittest.TestCase):
    """Test cases for WAV backend."""

    def test_wav_basic(self) -> None:
        """Test basic WAV file generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_output.wav'
            mf = DTMF()
            backend = WavBackend(output_path=output_path, sample_rate=8000.0)
            seq = Sequencer(
                mf=mf,
                backend=backend,
                pad_pause=0.0,
                sample_rate=8000.0,
                length=100,
                pause=50)
            seq('123')

            # Verify file was created
            self.assertTrue(output_path.exists())
            # Verify file has content
            self.assertGreater(output_path.stat().st_size, 0)

            # Verify WAV file is valid
            with wave.open(str(output_path), 'rb') as wav:
                self.assertEqual(wav.getnchannels(), 1)
                self.assertEqual(wav.getsampwidth(), 2)  # 16-bit
                self.assertEqual(wav.getframerate(), 8000)
                self.assertGreater(wav.getnframes(), 0)

    def test_wav_empty_sequence(self) -> None:
        """Test WAV backend with empty sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_empty.wav'
            mf = DTMF()
            backend = WavBackend(output_path=output_path)
            seq = Sequencer(
                mf=mf,
                backend=backend,
                pad_pause=0.0)
            seq('')

            # Empty sequence shouldn't create a file
            self.assertFalse(output_path.exists())

    def test_wav_long_sequence(self) -> None:
        """Test WAV backend with long sequence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_long.wav'
            mf = DTMF()
            backend = WavBackend(output_path=output_path, sample_rate=8000.0)
            seq = Sequencer(
                mf=mf,
                backend=backend,
                pad_pause=0.0,
                sample_rate=8000.0,
                length=50,
                pause=25)
            seq('1234567890' * 10)  # 100 tones

            # Verify file was created
            self.assertTrue(output_path.exists())

            # Verify WAV file has expected duration
            with wave.open(str(output_path), 'rb') as wav:
                # 100 tones * 50ms + 99 pauses * 25ms = 7475ms
                # At 8000 Hz: ~59800 samples
                frames = wav.getnframes()
                self.assertGreater(frames, 50000)
                self.assertLess(frames, 70000)

    def test_wav_clear_buffer(self) -> None:
        """Test clearing the buffer without writing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'test_clear.wav'
            backend = WavBackend(output_path=output_path)

            # Add some data
            backend.play(iter([0.1, 0.2, 0.3]), close=False)
            self.assertGreater(len(backend._buffer), 0)

            # Clear without writing
            backend.clear_buffer()
            self.assertEqual(len(backend._buffer), 0)

            # File should not exist
            self.assertFalse(output_path.exists())

    def test_wav_path_types(self) -> None:
        """Test that WAV backend accepts both str and Path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with Path
            output_path1 = Path(tmpdir) / 'test1.wav'
            backend1 = WavBackend(output_path=output_path1)
            self.assertEqual(backend1._output_path, output_path1)

            # Test with str
            output_path2 = str(Path(tmpdir) / 'test2.wav')
            backend2 = WavBackend(output_path=output_path2)
            self.assertIsInstance(backend2._output_path, Path)


if __name__ == '__main__':
    unittest.main()
