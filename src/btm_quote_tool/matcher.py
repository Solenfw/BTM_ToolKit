from .string_utilities import string_cleaner
from .file_operations import load_input
from .scorer import calculate_similarity
from .config import load_config
from logging import Logger

def stats_filter_out(product: dict[str, tuple[str, str]], keyword: str) -> dict[str, tuple[str, str]] | None:
    product_stats = {
        'cong': 'cvd',
        'thẳng': 'str',
        'cứng': 'rig',
        'răng cưa': 'serr',
        'vi phẫu' : 'micro',
        'mikro' : 'micro',
        'cán vàng' : 'tc',
        'tc' : 'tc',
    }
    filtered_product = {}

    avai_stats = [key for key in product_stats if key in keyword]
    if not avai_stats:
        return None

    for key, info in product.items():
        if all(product_stats[stat] in info[0] for stat in avai_stats):
            filtered_product[key] = info

    return filtered_product




# filter out family_names + name_tags
def name_filter_out(product_data: dict[str, tuple], keyword: str, words_included: list[str]) -> dict[str, tuple] | None:
    refined_options = [word for word in words_included if word in keyword]
    if not refined_options:
        return None

    # Filter product descriptions
    return {
        product: stats for product, stats in product_data.items()
        if any(word in product for word in refined_options)
    } or None



def find_best_match(general_log : Logger, score_log : Logger, keywords: list[str], product_data: dict[str, tuple]) -> tuple[list[str], list[str]]:
    product_codes, matched_products = [], []

    # Load configuration, family names, and name tags
    config = load_config()
    family_names, name_tags = load_input(config, 'data_source', 'family_name_file'), load_input(config, 'data_source', 'name_tag_file')

    # Process each keyword
    for index, keyword in enumerate(keywords):

        keyword_cleaned = string_cleaner(keyword)
        best_match, best_score = None, 0

        # Filter by family names or name tags
        name_filtered = name_filter_out(product_data, keyword_cleaned, family_names)
        tag_filtered = name_filter_out(product_data, keyword_cleaned, name_tags)

        # Use original product_data if filtering failed
        if tag_filtered and name_filtered:
            final_options = {**tag_filtered, **name_filtered}
        elif tag_filtered is not None:
            final_options = tag_filtered
        elif name_filtered is not None:
            final_options = name_filtered
        else:
            final_options = product_data

        temp_options = stats_filter_out(final_options, keyword_cleaned)
        final_options = temp_options or final_options

        # Calculate similarity for each product description
        for description in final_options.keys():
            similarity_score = calculate_similarity(keyword_cleaned, description)

            if similarity_score and similarity_score > best_score:
                best_score = similarity_score
                best_match = description

        # Append best match or "NONE" if no match is found
        if best_match:
            matched_products.append(best_match)
            product_codes.append(final_options[best_match][1])  
            general_log.info(f"INFO --> {index + 1} _product : {keyword}")
            general_log.info(f"       after cleaned : {keyword_cleaned}")
            general_log.info(f"     product matched : {best_match}")
            general_log.info(f"      matching score : {best_score}")
        else:
            matched_products.append("NONE")
            product_codes.append("NONE")
            general_log.info(f"     product matched : No suitable option found.")

    return product_codes, matched_products
