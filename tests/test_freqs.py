"""test_freqs.py

Tests for the freqs.py file.
"""

import unittest
import bluebox.freqs as freqs


class TestBaseMF(unittest.TestCase):
    """TestFreqs class for testing the BaseMF, DTMF and MF classes."""

    def test_base_mf(self) -> None:
        """Test the BaseMF class."""
        with self.assertRaises(TypeError):
            freqs.BaseMF()  # type: ignore

class TestDTMF(unittest.TestCase):
    def test_dtmf(self) -> None:
        """Test the DTMF class."""
        dtmf = freqs.DTMF()
        self.assertEqual(dtmf['1'], (697, 1209))
        self.assertEqual(dtmf['2'], (697, 1336))
        self.assertEqual(dtmf['3'], (697, 1477))
        self.assertEqual(dtmf['4'], (770, 1209))
        self.assertEqual(dtmf['5'], (770, 1336))
        self.assertEqual(dtmf['6'], (770, 1477))
        self.assertEqual(dtmf['7'], (852, 1209))
        self.assertEqual(dtmf['8'], (852, 1336))
        self.assertEqual(dtmf['9'], (852, 1477))
        self.assertEqual(dtmf['*'], (941, 1209))
        self.assertEqual(dtmf['0'], (941, 1336))
        self.assertEqual(dtmf['#'], (941, 1477))
        self.assertEqual(dtmf['A'], (697, 1633))
        self.assertEqual(dtmf['B'], (770, 1633))
        self.assertEqual(dtmf['C'], (852, 1633))
        self.assertEqual(dtmf['D'], (941, 1633))

        self.assertEqual(len(dtmf), 16)
        self.assertEqual(list(dtmf), list(dtmf._codes))
        self.assertEqual('1' in dtmf, True)
        self.assertEqual('D' in dtmf, True)
        self.assertNotEqual('E' in dtmf, True)


class TestMF(unittest.TestCase):
    mf_freqs = (700.0, 900.0, 1100.0, 1300.0, 1500.0, 1700.0)

    def test_mf(self) -> None:
        """Test the MF class."""
        mf = freqs.MF()
        self.assertEqual(mf['1'], (self.mf_freqs[0], self.mf_freqs[1]))
        self.assertEqual(mf['2'], (self.mf_freqs[0], self.mf_freqs[2]))
        self.assertEqual(mf['3'], (self.mf_freqs[1], self.mf_freqs[2]))
        self.assertEqual(mf['4'], (self.mf_freqs[0], self.mf_freqs[3]))
        self.assertEqual(mf['5'], (self.mf_freqs[1], self.mf_freqs[3]))
        self.assertEqual(mf['6'], (self.mf_freqs[2], self.mf_freqs[3]))
        self.assertEqual(mf['7'], (self.mf_freqs[0], self.mf_freqs[4]))
        self.assertEqual(mf['8'], (self.mf_freqs[1], self.mf_freqs[4]))
        self.assertEqual(mf['9'], (self.mf_freqs[2], self.mf_freqs[4]))
        self.assertEqual(mf['0'], (self.mf_freqs[3], self.mf_freqs[4]))
        self.assertEqual(mf['10'], (self.mf_freqs[3], self.mf_freqs[4]))
        self.assertEqual(mf['11'], (self.mf_freqs[0], self.mf_freqs[5]))
        self.assertEqual(mf['ST3'], (self.mf_freqs[0], self.mf_freqs[5]))
        self.assertEqual(mf['12'], (self.mf_freqs[1], self.mf_freqs[5]))
        self.assertEqual(mf['ST2'], (self.mf_freqs[1], self.mf_freqs[5]))
        self.assertEqual(mf['KP'], (self.mf_freqs[2], self.mf_freqs[5]))
        self.assertEqual(mf['KP2'], (self.mf_freqs[3], self.mf_freqs[5]))
        self.assertEqual(mf['ST'], (self.mf_freqs[4], self.mf_freqs[5]))

        self.assertEqual(len(mf), 15)
        self.assertEqual(list(mf), list(mf._codes))
        self.assertEqual('1' in mf, True)
        self.assertEqual('KP2' in mf, True)
        self.assertNotEqual('KP3' in mf, True)
