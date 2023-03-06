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
        seq = Sequencer(mf=mf)
        self.assertEqual(seq._mf, mf)
        self.assertEqual(seq._wave._sr, 44100.0)
        self.assertEqual(seq._wave._ch, 1)
        self.assertEqual(seq._length, 22.0)

    def test_sequencer_backend(self) -> None:
        """Test the Sequencer class with a backend."""
        mf = DTMF()
        seq = Sequencer(mf=mf, backend=DummyBackend)
        self.assertEqual(seq._mf, mf)
        self.assertEqual(seq._wave._sr, 44100.0)
        self.assertEqual(seq._wave._ch, 1)
        self.assertEqual(seq._length, 22.0)
        self.assertEqual(type(seq._backend), DummyBackend)

        # now with an initialized backend
        be = DummyBackend()
        seq = Sequencer(mf=mf, backend=be)
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
            pause=100)
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
            pause=100)
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
            pause=100)
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
            pause=100)
        seq('1')
        freq_pair_1 = mf['1']

        for i in range(5):
            self.assertAlmostEqual(
                be.get_data()[i],
                (math.sin(2*math.pi*freq_pair_1[0]*i/10) +
                    math.sin(2*math.pi*freq_pair_1[1]*i/10)) / 2)

        with self.assertRaises(IndexError):
            be.get_data()[5]
