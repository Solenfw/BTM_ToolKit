import re
import sys
from logging import Logger
from rapidfuzz import fuzz
sys.stdout.reconfigure(encoding='utf-8')


def fuzz_score(keyword: str, product: str) -> float:
    token_set_score = fuzz.token_set_ratio(keyword, product)
    simple_ratio_score = fuzz.ratio(keyword, product)
    weighted_score = (0.8 * token_set_score) + (0.2 * simple_ratio_score)
    return round(weighted_score, 2)

def size_matching_score(keyword: str, product: str) -> float:
    pattern = r'(dài)\s+(\d+(\.\d+)?)\s*(mm|cm)'

    key_match = re.search(pattern, keyword)
    product_match = re.search(pattern, product)

    if not key_match or not product_match:
        return 0.0

    key_size = float(key_match.group(2))
    product_size = float(product_match.group(2))

    # Allow a tolerance margin (e.g., 0.1) for minor variations
    margin = abs(key_size - product_size)
    tolerance = 0.5
    return 100.0 if margin <= tolerance else max(0.0, 100.0 / (margin + 1))


def tip_matching_score(keyword: str, product: str) -> float:
    pattern = r'(đầu)\s+(\d+(\.\d+)?)\s*(mm)'

    key_match = re.search(pattern, keyword)
    product_match = re.search(pattern, product)

    if not key_match or not product_match:
        return 0.0

    key_tip = float(key_match.group(2))
    product_tip = float(product_match.group(2))

    # Same tolerance for the tip
    margin = abs(key_tip - product_tip)
    tolerance = 0.5
    return 100.0 if margin <= tolerance else max(0.0, 100.0 / (margin + 1))

def calculate_similarity(keyword: str, product: str) -> float | None:
    similarity = fuzz_score(keyword, product)
    size_score = size_matching_score(keyword, product)
    tip_score = tip_matching_score(keyword, product)

    final_score = 0

    if tip_score:
        final_score += tip_score * 0.1 + similarity * 0.6 + size_score * 0.3
    elif size_score:
        final_score += size_score * 0.3 + similarity * 0.7
    else:
        final_score += similarity

    return round(final_score, 2) if final_score >= 80 else None

