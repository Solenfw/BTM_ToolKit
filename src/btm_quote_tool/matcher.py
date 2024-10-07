from fuzzywuzzy import fuzz
from .string_utilities import *


def calculate_similarity(keyword: str, product: str) -> int:
    """Validates and scores the similarity between a keyword and a product description."""
    keyword = string_cleaner(keyword)
    product = string_cleaner(product)

    # Check for a perfect match based on word containment
    keywords = keyword.split()
    if all_keywords_exist(keywords, product):
        return 200

    score = fuzz.token_set_ratio(keyword, product) + fuzz.ratio(keyword, product)
    return score


def find_best_match(keywords, product_data) -> list[str]:
    """Finds the best matching product for each keyword."""
    product_codes = []
    matched_products = []

    for keyword in keywords:
        best_match = None
        best_score = 0
        
        for description in product_data.keys():
            similarity_score = calculate_similarity(keyword, description)
            if similarity_score >= 130 and similarity_score > best_score:
                best_score = similarity_score
                best_match = description

        if best_match:
            matched_products.append(best_match)
            product_codes.append(product_data[best_match][1])  
        else:
            product_codes.append("NONE")
            matched_products.append('NONE')
    
    return product_codes, matched_products