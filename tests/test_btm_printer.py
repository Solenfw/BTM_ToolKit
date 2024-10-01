import io
import sys
import os
import unittest
from contextlib import redirect_stdout

# Add the `src/` directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from btm_quote_tool.btm_printer import print_btm_3d

class TestBTMPrinter(unittest.TestCase):
    def test_print_btm_3d(self):
        """
        Test the print_btm_3d function to check if it prints the correct output.
        """
        expected_output = (
            "BBBB    TTTTT   M   M\n"
            "B   B     T     MM MM\n"
            "BBBB      T     M M M\n"
            "B   B     T     M   M\n"
            "BBBB      T     M   M\n"
        )

        # Capture the output
        f = io.StringIO()
        with redirect_stdout(f):
            print_btm_3d()
        output = f.getvalue()

        # Compare output
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
