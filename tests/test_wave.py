"""test_wave.py

Tests for the wave.py file.
"""

import unittest
import bluebox.wave as wave
import math


class TestWave(unittest.TestCase):
    """TestWave class for testing the wave.py file."""

    def test_sine(self) -> None:
        """Test the sine wave generator."""

        sine = wave.SineWave(sample_rate=10)
        sine_wave = sine.sine(freq=5, length=1000, amplitude=1.0, phase=0.0)
        sine_wave = list(sine_wave)
        self.assertEqual(len(sine_wave), 10)
        self.assertEqual(sine_wave[0], 0.0)
        for i in range(1, 10):
            self.assertAlmostEqual(
                sine_wave[i],
                math.sin(2 * math.pi * 5 * i / 10))

    def test_sine_zero(self) -> None:
        """Test the sine wave generator with zero frequency."""

        sine = wave.SineWave(sample_rate=10)
        sine_wave = sine.sine(freq=0, length=1000, amplitude=1.0, phase=0.0)
        sine_wave = list(sine_wave)
        self.assertEqual(len(sine_wave), 10)
        for i in range(10):
            self.assertEqual(sine_wave[i], 0.0)

        sine = wave.SineWave(sample_rate=10)
        sine_wave = sine.sine(freq=5, length=1000, amplitude=0.0, phase=0.0)
        sine_wave = list(sine_wave)
        self.assertEqual(len(sine_wave), 10)
        for i in range(10):
            self.assertEqual(sine_wave[i], 0.0)

    def test_sine_call(self) -> None:
        """Test the sine wave generator."""

        sine = wave.SineWave(sample_rate=100)
        sine_wave = sine(freq=5, length=1000, amplitude=1.0, phase=0.0)
        sine_wave = list(sine_wave)
        self.assertEqual(len(sine_wave), 100)
        self.assertEqual(sine_wave[0], 0.0)
        for i in range(1, 100):
            self.assertAlmostEqual(
                sine_wave[i],
                math.sin(2 * math.pi * 5 * i / 100))
