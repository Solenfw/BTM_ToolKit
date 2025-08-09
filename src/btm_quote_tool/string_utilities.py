import re

# special cases of substrings
substring_replacements = {
    'hoặc tương đương' : '',
    'nhíp': 'kẹp',
    'kềm' : 'kìm',
    'nhíp mô': 'kẹp phẫu tích mô',
    'kẹp mang kim': 'kìm kẹp kim',
    'kẹp cầm máu' : 'kẹp mạch máu',
    'kìm mang kim': 'kìm kẹp kim',
    'kẹp động mạch': 'kẹp mạch máu',
    'khay đựng hình quả thận': 'đĩa thận',
    'khay quả thận' : 'đĩa thận',
    'khay thận' : 'đĩa thận',
    'vòng giữ dụng cụ có cán vòng' : 'kim băng cài giữ dụng cụ',
    'bát tròn' : 'chén tròn',
    'Cốc đựng dung dịch' : 'cốc đo có chia vạch',
    'Cốc đo dung tích' : 'cốc đo có chia vạch',
    'Đệm giữ silicon' : 'tấm silicone'
}


def all_keywords_exist(keywords: list, check_string: str) -> bool:
    """Checks if all words from a keyword are present in the target string."""
    return all(keyword in check_string for keyword in keywords)



def string_cleaner(text: str) -> str:
    text = str(text)
    """Cleans and standardizes input text for comparison."""
    if not re.search(r'\d{2}-\d{3}-\d{2}-\d{2}', text):
        text = re.sub(r'[^\w\.\\\/°]', ' ', text).strip()             # Remove special characters
    elif len(text) <= 10 or "load" in text:
         text = re.sub(r'[^\w\.\\\/-]', ' ', text).strip()  
    else:
        text = re.sub(r'[^\w-]', ' ', text).strip() 
    text = re.sub(r'\s+', ' ', text).strip().lower()               # Normalize whitespace and case
    
    # Apply substring replacements
    for original, sub in substring_replacements.items():
        original_text = re.sub(r'\s+', ' ', original).strip().lower()
        replacement = re.sub(r'\s+', ' ', sub).strip().lower()
        text = text.replace(original_text, replacement) if original_text in text else text

    # stats format
    text = size_format(text)
    text = tip_format(text)
    text = box_format(text)

    return text


def size_format(input_str: str) -> str:
    pattern = r'(dài)\s+(\d+(\.\d+)?)\s*(mm|cm)'  # Pattern to match sizes with units (mm or cm)
    match = re.search(pattern, input_str)
    if not match:
        return input_str  # Return the original string if no match is found

    def mm_to_cm(match):
        value = float(match.group(2))  # Extract the numeric value
        unit = match.group(4)  # Extract the unit (mm or cm)
        if unit == 'mm':
            cm_value = value / 10.0  # Convert mm to cm
        else:
            cm_value = value  # If already in cm, no conversion needed
        # Return the value formatted to one decimal place if it's not an integer
        return f"dài {cm_value:.1f} cm" if cm_value % 1 else f"{int(cm_value)} cm"

    # Substitute matches with the converted value
    result = re.sub(pattern, mm_to_cm, input_str)
    return result


def tip_format(text: str) -> str:
    pattern = r'(đầu|kích thước)\s+(\d+(\.\d+)?)\s*(mm)'
    match = re.search(pattern, text)
    if not match:
        return text
    modified_text = re.sub(pattern, r'\1 \2 \4', text)
    return modified_text


def box_format(text : str) -> str:
    pattern = r'(\d{3})\s*x\s*(\d{3})\s*x\s*(\d{2})\s*(mm)'
    match = re.search(pattern, text)
    if not match:
        return text

    modified_text = re.sub(pattern, r'\1x\2x\3 \4', text)
    return modified_text