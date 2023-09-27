import sys
import unittest

from beerpong.cli.cli import main as cli_main


class TestCLI(unittest.TestCase):
    def test_wrong_script(self):
        sys.argv = ["beerong", "wrong_script"]
        with self.assertRaises(ValueError):
            cli_main()

    def test_warns_in_debug_mode(self):
        sys.argv = ["beerong", "wrong_script"]
        # Catch ValueError due to wrong script name. Otherwise,
        # the benchmark would be run.
        with self.assertWarns(RuntimeWarning) and self.assertRaises(ValueError):
            cli_main()

    def test_noop(self):
        sys.argv = ["beerong", "noop"]
        cli_main()
