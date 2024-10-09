from fuzzywuzzy import fuzz
from typing import Tuple, List, Dict
from pathlib import Path
from .string_utilities import string_cleaner, all_keywords_exist
from .config import load_config
import logging


def calculate_similarity(keyword: str, product: str) -> int:
    # Check for a perfect match based on word containment
    if all_keywords_exist(keyword.split(), product):
        return 1000
    # Calculate a fuzzy matching score
    score = fuzz.token_set_ratio(keyword, product) + fuzz.ratio(keyword, product)
    return score



def filter_out(product_data: Dict[str, Tuple], keyword: str, words_included: List[str]) -> Dict[str, Tuple]:
    refined_options = [word for word in words_included if word in keyword]
    if not refined_options:
        return None

    # Filter product descriptions that contain any of the refined options
    filtered_products = {
        product: stats
        for product, stats in product_data.items()
        if any(word in product for word in refined_options)
    }
    # Return the filtered results or the original product data if no matches
    return filtered_products if filtered_products else None



def find_best_match(keywords: List[str], product_data: Dict[str, Tuple]) -> Tuple[List[str], List[str]]:
    product_codes = []
    matched_products = []

    # Load configuration and family/name tag files
    config = load_config()
    family_name_file = Path(config['family_name_file']).resolve()
    name_tag_file = Path(config['name_tag_file']).resolve()

    # Read family names and name tags
    with open(family_name_file, 'r', encoding='utf-8') as f:
        family_names = [line for line in f.read().splitlines()]

    with open(name_tag_file, 'r', encoding='utf-8') as f:
        name_tags = [tag for tag in f.read().splitlines()]


    # Process each keyword
    for index, keyword in enumerate(keywords):
        logging.info (f"INFO --> {index + 1} _ product : {keyword}")
        keyword = string_cleaner(keyword)
        best_match = None
        best_score = 0
        
        # Filter products by family names, then by name tags in case no family name found
        name_filtered_options = filter_out(product_data, keyword, family_names)
        tag_filtered_options = filter_out(product_data, keyword, name_tags)

        # Use full product data if filtering failed
        if tag_filtered_options is not None and name_filtered_options is not None:
            final_options = {**tag_filtered_options, **name_filtered_options}
        elif tag_filtered_options is not None:
            final_options = tag_filtered_options
        elif name_filtered_options is not None:
            final_options = name_filtered_options
        else:
            final_options = product_data
        
        # Calculate similarity for each product description
        for description in final_options.keys():
            description_clean = string_cleaner(description)
            similarity_score = calculate_similarity(keyword, description_clean)

            if similarity_score > best_score:
                best_score = similarity_score
                best_match = description

        # Append the best match or "NONE" if no match is found
        if best_match:
            matched_products.append(best_match)
            product_codes.append(final_options[best_match][1])  # Assuming product code is at index 1
        else:
            matched_products.append("NONE")
            product_codes.append("NONE")

    return product_codes, matched_products
