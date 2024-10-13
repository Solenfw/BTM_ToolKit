import re
import sys
from fuzzywuzzy import fuzz
sys.stdout.reconfigure(encoding='utf-8')

def fuzz_score(keyword: str, product: str) -> float:
    token_set_score = fuzz.token_set_ratio(keyword, product)
    simple_ratio_score = fuzz.ratio(keyword, product)

    weighted_score = (0.7 * token_set_score) + (0.3 * simple_ratio_score)
    return round(weighted_score, 2)


# need to throughly check before adding in the workflow
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


def tray_value_matching(keyword_match: re.Match, product_match: re.Match) -> float:
    try:
        key_length, key_width, key_height = map(int, keyword_match.groups()[:-1])
        length, width, height = map(int, product_match.groups()[:-1])
    except (ValueError, TypeError):
        return 0.0

    length_margin = abs(key_length - length)
    width_margin = abs(key_width - width)
    height_margin = abs(key_height - height)

    max_length = max(key_length, length)
    max_width = max(key_width, width)
    max_height = max(key_height, height)

    score = (
            (1 - (length_margin / max_length)) * 0.4 +  # Length has higher weight
            (1 - (width_margin / max_width)) * 0.3 +  # Width has medium weight
            (1 - (height_margin / max_height)) * 0.3  # Height has medium weight
    )
    return round(score, 2)


def tray_matching_score(keyword: str, product: str) -> float:
    patterns = [
        r'(\d{3})\s*x\s*(\d{3})\s*x\s*(\d{2})\s*(mm)',
        r'(\d{3})\s*x\s*(\d{3})\s*x\s*(\d{3})\s*(mm)',
        r'(\d{2})\s*x\s*(\d{2})\s*x\s*(\d{2})\s*(mm)'
    ]

    for pattern in patterns:
        keyword_match = re.search(pattern, keyword)
        product_match = re.search(pattern, product)

        if keyword_match and product_match:
            return tray_value_matching(keyword_match, product_match)
    return 0.0


def calculate_similarity(keyword: str, product: str) -> float:
    similarity = fuzz_score(keyword, product)
    size_score = size_matching_score(keyword, product)
    tip_score = tip_matching_score(keyword, product)
    tray_score = tray_matching_score(keyword, product)

    final_score = 0

    if tip_score:
        final_score += tip_score * 0.1 + similarity * 0.6 + size_score * 0.3 + tray_score
    else:
        final_score += size_score * 0.3 + similarity * 0.7 + tray_score
    return round(final_score, 2)

