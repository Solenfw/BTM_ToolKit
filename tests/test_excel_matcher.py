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
        print(sys.path)
        # Get the absolute path for the result directory
        result_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'result/'))
        product_file = os.path.join(result_dir, 'product.txt')
        expected_file = os.path.join(result_dir, 'expected_product.txt')
        self.unmatched_file = os.path.join(result_dir, 'unmatched.txt')

        with open(product_file, 'r', encoding='utf-8') as file1, open(expected_file, 'r', encoding='utf-8') as file2:
            self.product = [string_cleaner(line) for line in file1.readlines()]
            self.expected_product = [string_cleaner(line) for line in file2.readlines()]


    def test_product_family_matching(self):
        with open(self.unmatched_file, 'w', encoding='utf-8') as file:
            for product, expected in zip(self.product, self.expected_product):
                if fuzz.token_set_ratio(product, expected) < 90:
                    self.assertNotEqual(product, expected)
                    file.write(product + '\n')
    
        

if __name__ == '__main__':
    unittest.main()
