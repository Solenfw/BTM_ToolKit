from fuzzywuzzy import fuzz
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
from .string_utilities import all_keywords_exist


def calculate_similarity(keyword: str, product: str) -> int:
    keywords_list = keyword.split()
    if all_keywords_exist(keywords_list, product):
        return 1000
    # Fuzzy matching score
    return fuzz.token_set_ratio(keyword, product) + fuzz.ratio(keyword, product) + size_matching_score(keyword, product)



def size_matching_score(keyword: str, product: str) -> float:
    pattern = r'(dài)\s+(\d+(\.\d+)?)\s*(mm|cm)'

    key_match = re.search(pattern, keyword)
    product_match = re.search(pattern, product)

    if not key_match or not product_match:
        return 0.0

    key_size = float(key_match.group(2))
    product_size = float(product_match.group(2))
    margin = abs(key_size - product_size)
    return 100.0 if margin == 0 else 100.0 / margin