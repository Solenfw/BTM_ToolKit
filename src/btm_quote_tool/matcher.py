from typing import Tuple, List, Dict
from .string_utilities import string_cleaner, size_format
from .file_operations import load_input
from .scorer import calculate_similarity
from .config import load_config
import logging



# filter out family_names + name_tags
def filter_out(product_data: Dict[str, Tuple], keyword: str, words_included: List[str]) -> Dict[str, Tuple]:
    refined_options = [word for word in words_included if word in keyword]
    if not refined_options:
        return None

    # Filter product descriptions
    return {
        product: stats for product, stats in product_data.items()
        if any(word in product for word in refined_options)
    } or None



def find_best_match(keywords: List[str], product_data: Dict[str, Tuple]) -> Tuple[List[str], List[str]]:
    product_codes, matched_products = [], []

    # Load configuration, family names, and name tags
    config = load_config()
    family_names, name_tags = load_input(config, 'data_source', 'family_name_file'), load_input(config, 'data_source', 'name_tag_file')

    # Process each keyword
    for index, keyword in enumerate(keywords):
        logging.info(f"INFO --> {index + 1} _ product : {keyword}")

        keyword_cleaned = string_cleaner(keyword)
        keyword_cleaned = size_format(keyword_cleaned)
        best_match, best_score = None, 0
        logging.info(f"REF --> after cleaned : {keyword_cleaned}")

        # Filter by family names or name tags
        name_filtered = filter_out(product_data, keyword_cleaned, family_names)
        tag_filtered = filter_out(product_data, keyword_cleaned, name_tags)

        # Use original product_data if filtering failed
        if tag_filtered and name_filtered:
            final_options = {**tag_filtered, **name_filtered}
        elif tag_filtered is not None:
            final_options = tag_filtered
        elif name_filtered is not None:
            final_options = name_filtered
        else:
            final_options = product_data

        # Calculate similarity for each product description
        for description in final_options.keys():
            description_cleaned = string_cleaner(description)
            description_cleaned = size_format(description_cleaned)
            similarity_score = calculate_similarity(keyword_cleaned, description_cleaned)

            if similarity_score > best_score:
                best_score = similarity_score
                best_match = description

        # Append best match or "NONE" if no match is found
        if best_match:
            matched_products.append(best_match)
            product_codes.append(final_options[best_match][1])  # Assuming product code at index 1
        else:
            matched_products.append("NONE")
            product_codes.append("NONE")

    return product_codes, matched_products
