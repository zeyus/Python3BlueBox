"""test_cli.py

Tests for the cli.
"""

import unittest
import bluebox.cli as cli


class TestCLI(unittest.TestCase):
    """Make sure the CLI works as expected"""

    def test_bluebox_cli(self) -> None:
        """Test the CLI"""

        # test help
        with self.assertRaises(SystemExit):
            cli.bluebox(cli.parse_args(['-h']))

        # test version
        with self.assertRaises(SystemExit):
            cli.bluebox(cli.parse_args(['-v']))
