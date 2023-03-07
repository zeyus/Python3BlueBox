"""freqs.py

This file contains frequency information for the BlueBox
as well as frequency manupulation functions.
"""

import typing as t
from abc import ABC, abstractmethod
import math


class BaseMF(ABC):
    """BaseMF class for defining MF frequencies."""

    _col: t.Tuple[float, ...]
    _row: t.Tuple[float, ...]
    _codes: t.Tuple[str, ...]
    _size: t.Tuple[int, int]

    def __init__(self) -> None:
        super().__init__()
        self._size = (len(self._col), len(self._row))

    def valid_codes(self) -> t.Set[str]:
        """Get the valid codes."""
        return set(self._codes)

    @abstractmethod
    def __getitem__(self, key: str) -> t.Tuple[float, float]:
        """Get the frequencies for a given code."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Get the number of codes."""
        return len(self._codes)

    def __iter__(self) -> t.Iterator[str]:
        """Iterate over the codes."""
        return iter(self._codes)

    def __contains__(self, key: str) -> bool:
        """Check if a code is valid."""
        return key in self._codes

    def __repr__(self) -> str:
        """Get the representation of the MF."""
        return f'{self.__class__.__name__}({self._codes})'


class DTMF(BaseMF):
    """DTMF implementation of BaseMF."""

    _col = (697.0, 770.0, 852.0, 941.0)
    _row = (1209.0, 1336.0, 1477.0, 1633.0)
    _codes = (
        '1', '2', '3', 'A',
        '4', '5', '6', 'B',
        '7', '8', '9', 'C',
        '*', '0', '#', 'D')

    def __getitem__(self, key: str) -> t.Tuple[float, float]:
        """Get the DTMF frequencies for a given code."""
        if key not in self._codes:
            raise KeyError(f'Invalid code: {key}')
        return (self._col[self._codes.index(key) // self._size[0]],
                self._row[self._codes.index(key) % self._size[1]])


"""
The following is an implementation of the old MF standard.

This is out of curiosity but also as an implementation example.

In the Multi-Frequency (MF) signaling, the frequency pairs are used to
represent the telephone keypad digits. There are three MF standards,
namely MF 2/5, MF 2/6, and MF 2/8, which differ in the number of frequency
pairs used and the frequency range.

MF 2/8 standard uses eight frequency pairs in the frequency range of
700 Hz to 1700 Hz with a spacing of 100 Hz between adjacent frequencies.
The eight frequency pairs are used to represent the digits 0 to 9 on the
telephone keypad, with additional codes 11, 12, KP, KP2, ST as follows:

    - 700 Hz and 900 Hz for digit 1
    - 700 Hz and 1100 Hz for digit 2
    - 900 Hz and 1100 Hz for digit 3
    - 700 Hz and 1300 Hz for digit 4
    - 900 Hz and 1300 Hz for digit 5
    - 1100 Hz and 1300 Hz for digit 6
    - 700 Hz and 1500 Hz for digit 7
    - 900 Hz and 1500 Hz for digit 8
    - 1100 Hz and 1500 Hz for digit 9
    - 1300 Hz and 1500 Hz for digit 0 / 10
    - 700 Hz and 1700 Hz for code 11 / ST3
    - 900 Hz and 1700 Hz for code 12 / ST2
    - 1100 Hz and 1700 Hz for code KP
    - 1300 Hz and 1700 Hz for code KP2
    - 1500 Hz and 1700 Hz for code ST

"""


class MF(BaseMF):
    """MF implementation of BaseMF."""

    _col = (700.0, 900.0, 1100.0, 1300.0, 1500.0, 1700.0)
    _codes = (
        '1', '2', '3',
        '4', '5', '6',
        '7', '8', '9',
        '0', '11', '12',
        'KP', 'KP2', 'ST')
    _alt_codes: t.Tuple[t.Union[str, None], ...] = (
        None, None, None,
        None, None, None,
        None, None, None,
        '10', 'ST3', 'ST2',
        None, None, None)

    def __init__(self, ) -> None:
        self._row = self._col
        super().__init__()

    def valid_codes(self) -> t.Set[str]:
        return set(
            self._codes +
            tuple(c for c in self._alt_codes if c is not None))

    def __getitem__(self, key: str) -> t.Tuple[float, float]:
        """Get the MF frequencies for a given code."""

        # ensure code is valid
        if key not in self._codes and key not in self._alt_codes:
            raise KeyError(f'Invalid code: {key}')

        # get index of code
        idx = self._codes.index(key) if key in self._codes else self._alt_codes.index(key)  # noqa: E501

        col_idx = int((math.sqrt(1 + 8 * idx) - 1) / 2)
        row_idx = idx - (col_idx * (col_idx + 1)) // 2

        # return frequency pair
        return (self._row[row_idx], self._col[col_idx+1])
