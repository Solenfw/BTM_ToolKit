import os
import sys
import unittest
from fuzzywuzzy import fuzz

# Add source directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from BTM_Quote_Tool.string_utilities import string_cleaner

class Color():
    CYAN = '\033[1;36m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    RED = '\033[1;91m'
    END = '\033[0m'  


class TestExcelMatcher(unittest.TestCase):

    def setUp(self):
        os.system("")
        with open('result/product.txt', 'r', encoding='utf-8') as file1, open("result/expected_product.txt", 'r', encoding='utf-8') as file2:
            self.product = [string_cleaner(line) for line in file1.readlines()]
            self.expected_product = [string_cleaner(line) for line in file2.readlines()]

    def test_product_family_matching(self):
        mismatches = [] 
        with open("result/unmatched.txt", 'w', encoding='utf-8') as file:
            for index, (product, expected) in enumerate(zip(self.product, self.expected_product), start=1):
                if fuzz.token_set_ratio(product, expected) < 90:
                    mismatches.append(f"Line {index}: {Color.RED}{product}{Color.END} != {Color.YELLOW}{expected}{Color.END}")
                    file.write(product + '\n')
        
        if mismatches:
            self.fail(f"Mismatches found:\n" + "\n".join(mismatches))

        

if __name__ == '__main__':
    unittest.main()
