import os
import sys
import unittest
from fuzzywuzzy import fuzz
# Add source directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

class Color():
    CYAN = '\033[1;36m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    RED = '\033[1;91m'
    END = '\033[0m'  


class TestExcelMatcher(unittest.TestCase):
    pass
        

if __name__ == '__main__':
    unittest.main()
