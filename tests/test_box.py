"""test_box.py

Tests for the box.py file.
"""

import unittest
import math
from bluebox.box import Sequencer
from bluebox.freqs import DTMF
from bluebox.backends.backend_dummy import DummyBackend


class TestSequencer(unittest.TestCase):
    """TestSequencer class for testing the box Sequencer"""

    def test_sequencer(self) -> None:
        """Test the Sequencer class."""
        mf = DTMF()
        seq = Sequencer(mf=mf, pad_pause=0.0)
        self.assertEqual(seq._mf, mf)
        self.assertEqual(seq._wave._sr, 44100.0)
        self.assertEqual(seq._wave._ch, 1)
        self.assertEqual(seq._length, 22.0)

    def test_sequencer_backend(self) -> None:
        """Test the Sequencer class with a backend."""
        mf = DTMF()
        seq = Sequencer(mf=mf, backend=DummyBackend,
                        pad_pause=0.0)
        self.assertEqual(seq._mf, mf)
        self.assertEqual(seq._wave._sr, 44100.0)
        self.assertEqual(seq._wave._ch, 1)
        self.assertEqual(seq._length, 22.0)
        self.assertEqual(type(seq._backend), DummyBackend)

        # now with an initialized backend
        be = DummyBackend()
        seq = Sequencer(mf=mf, backend=be,
                        pad_pause=0.0)
        self.assertEqual(seq._mf, mf)
        self.assertEqual(seq._wave._sr, 44100.0)
        self.assertEqual(seq._wave._ch, 1)
        self.assertEqual(seq._length, 22.0)
        self.assertEqual(seq._backend, be)

    def test_sequencer_output(self) -> None:
        """Test the Sequencer class with a backend."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=0.0)
        seq('1234')

        # check the output (4 tones, 5 samples each, 3 samples pause)
        self.assertEqual(len(be.get_data()), 4*5 + 3*1)

    def test_sequencer_output2(self) -> None:
        """Test the Sequencer class with a backend."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=0.0)
        seq('1234')
        seq('6789')

        # check the output (4 tones, 5 samples each, 3 samples pause)
        self.assertEqual(len(be.get_data()), 2*(4*5 + 3*1))

    def test_mf_values(self) -> None:
        """Test the values of the sequencer line up with the DTMF values."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=0.0)
        seq('12')
        freq_pair_1 = mf['1']
        freq_pair_2 = mf['2']

        for i in range(5):
            self.assertAlmostEqual(
                be.get_data()[i],
                (math.sin(2*math.pi*freq_pair_1[0]*i/10) +
                    math.sin(2*math.pi*freq_pair_1[1]*i/10)) / 2)
            self.assertAlmostEqual(
                be.get_data()[6+i],
                (math.sin(2*math.pi*freq_pair_2[0]*i/10) +
                    math.sin(2*math.pi*freq_pair_2[1]*i/10)) / 2)

        self.assertEqual(be.get_data()[5], 0.0)

        with self.assertRaises(IndexError):
            be.get_data()[11]

    def test_mf_values_single_tone(self) -> None:
        """Test the values of the sequencer line up with the DTMF values."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=0.0)
        seq('1')
        freq_pair_1 = mf['1']

        for i in range(5):
            self.assertAlmostEqual(
                be.get_data()[i],
                (math.sin(2*math.pi*freq_pair_1[0]*i/10) +
                    math.sin(2*math.pi*freq_pair_1[1]*i/10)) / 2)

        with self.assertRaises(IndexError):
            be.get_data()[5]

    def test_pad_pause(self) -> None:
        """Test the pad_pause parameter."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=0.0)
        seq('1')
        self.assertEqual(len(be.get_data()), 5)

        be.clear_data()
        seq = Sequencer(
            mf=mf,
            backend=be,
            sample_rate=10.0,
            length=500,
            pause=100,
            pad_pause=500)  # ms
        seq('1')
        self.assertEqual(len(be.get_data()), 5+10)

    def test_empty_sequence(self) -> None:
        """Test handling of empty sequence."""
        mf = DTMF()
        be = DummyBackend(mode='list')
        seq = Sequencer(mf=mf, backend=be, pad_pause=0.0)
        seq('')
        self.assertEqual(len(be.get_data()), 0)

    def test_invalid_characters_non_stop(self) -> None:
        """Test handling of invalid characters with stop_on_error=False."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            stop_on_error=False,
            pad_pause=0.0,
            sample_rate=10.0,
            length=500,
            pause=100)
        seq('1X2Y3')  # X and Y are invalid
        # Should only play 1, 2, 3 (3 tones * 5 samples + 2 pauses * 1 sample)
        self.assertEqual(len(be.get_data()), 3*5 + 2*1)

    def test_invalid_characters_stop(self) -> None:
        """Test handling of invalid characters with stop_on_error=True."""
        mf = DTMF()
        be = DummyBackend(mode='list')
        seq = Sequencer(mf=mf, backend=be, stop_on_error=True, pad_pause=0.0)
        with self.assertRaises(ValueError) as cm:
            seq('1X2')
        self.assertIn('Invalid code', str(cm.exception))
        self.assertIn('position 1', str(cm.exception))

    def test_negative_amplitude(self) -> None:
        """Test validation of negative amplitude."""
        mf = DTMF()
        with self.assertRaises(ValueError) as cm:
            Sequencer(mf=mf, amplitude=-0.5)
        self.assertIn('Amplitude', str(cm.exception))

    def test_zero_amplitude(self) -> None:
        """Test validation of zero amplitude."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, amplitude=0.0)

    def test_amplitude_too_high(self) -> None:
        """Test validation of amplitude > 1.0."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, amplitude=1.5)

    def test_negative_length(self) -> None:
        """Test validation of negative length."""
        mf = DTMF()
        with self.assertRaises(ValueError) as cm:
            Sequencer(mf=mf, length=-10)
        self.assertIn('Length', str(cm.exception))

    def test_negative_pause(self) -> None:
        """Test validation of negative pause."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, pause=-10)

    def test_negative_sample_rate(self) -> None:
        """Test validation of negative sample rate."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, sample_rate=-100)

    def test_zero_channels(self) -> None:
        """Test validation of zero channels."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, channels=0)

    def test_negative_pad_pause(self) -> None:
        """Test validation of negative pad pause."""
        mf = DTMF()
        with self.assertRaises(ValueError):
            Sequencer(mf=mf, pad_pause=-10)

    def test_long_sequence(self) -> None:
        """Test handling of very long sequences."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            pad_pause=0.0,
            sample_rate=10.0,
            length=100,  # 1 sample
            pause=100)   # 1 sample
        seq('1' * 100)  # 100 tones
        # 100 tones * 1 sample + 99 pauses * 1 sample = 199 samples
        self.assertEqual(len(be.get_data()), 199)

    def test_pause_logic_with_invalid_codes(self) -> None:
        """Test pause logic works correctly when invalid codes present."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            stop_on_error=False,
            pad_pause=0.0,
            sample_rate=10.0,
            length=500,
            pause=100)
        # '1', 'X' (invalid), '2', 'Y' (invalid), '3'
        # Should play: 1, pause, 2, pause, 3
        seq('1X2Y3')
        self.assertEqual(len(be.get_data()), 3*5 + 2*1)

    def test_metacode_pause(self) -> None:
        """Test that metacodes (p, P) insert pauses."""
        mf = DTMF()
        be = DummyBackend(mode='list', sample_rate=10.0)
        seq = Sequencer(
            mf=mf,
            backend=be,
            pad_pause=0.0,
            sample_rate=10.0,
            length=500,
            pause=100)
        seq('1p2')
        # Should play: tone1, pause, metacode pause (counts as valid
        # code), pause, tone2
        # 2 tones * 5 samples + 3 pauses * 1 sample = 13 samples
        self.assertEqual(len(be.get_data()), 2*5 + 3*1)
