import re

# special cases of substrings
substring_replacements = {
    'xám' : 'bạc',
    'nhíp': 'kẹp',
    'nhíp mô': 'kẹp phẫu tích mô',
    'kẹp mang kim': 'kìm kẹp kim',
    'kẹp động mạch': 'kẹp mạch máu',
    'cán dao mổ': 'cán dao phẫu thuật',
    'nẩy xương': 'bẩy xương',
    'khay đựng hình quả thận': 'đĩa thận',
    'vén não': 'thìa phẫu thuật',
    'vén rễ thần kinh': 'móc',
    'vòng giữ dụng cụ có cán vòng' : 'kim băng cài giữ dụng cụ',
    'đáy hộp đựng và bảo quản dụng cụ phẫu thuật' : 'đáy hộp đựng và bảo quản dụng cụ',
    'Hộp hấp đựng và bảo quản dụng cụ phẫu thuật' : 'Hộp đựng và bảo quản dụng cụ',
    'khay lưới bảo quản dụng cụ phẫu thuật' : 'khay lưới đựng dụng cụ',
    'khay lưới đựng dụng cụ phẫu thuật' : 'khay lưới đựng dụng cụ',
    'nắp hộp đựng và bảo quản dụng cụ phẫu thuật' : 'nắp hộp đựng và bảo quản dụng cụ',
    'Que thăm' : 'que nong',
    'bát tròn' : 'chén tròn',
    'thìa nạo tử cung' : 'nạo tử cung'
}


def all_keywords_exist(keywords: list, check_string: str) -> bool:
    """Checks if all words from a keyword are present in the target string."""
    return all(keyword in check_string for keyword in keywords)



def string_cleaner(text: str) -> str:
    """Cleans and standardizes input text for comparison."""
    text = re.sub(r'[^\w\s/.-]', '', text)                 # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip().lower()       # Normalize whitespace and case
    
    # Apply substring replacements
    for original, sub in substring_replacements.items():
        original_text = re.sub(r'\s+', ' ', original).strip().lower()
        replacement = re.sub(r'\s+', ' ', sub).strip().lower()
        text = text.replace(original_text, replacement) if original_text in text else text
    return text


def size_format(input_str: str) -> str:
    pattern = r'(dài)\s+(\d+(\.\d+)?)\s*(mm|cm)'
    
    def mm_to_cm(match):
        if match.group(4) == 'mm':
            mm_value = float(match.group(2))
            cm_value = mm_value / 10.0
            if cm_value.is_integer():
                return f"{match.group(1)} {int(cm_value)} cm"
            else:
                return f"{match.group(1)} {cm_value:.1f} cm"
        else:
            cm_value = float(match.group(2))
            if cm_value.is_integer():
                return f"{match.group(1)} {int(cm_value)} cm"
            else:
                return f"{match.group(1)} {cm_value:.1f} cm"

    result = re.sub(pattern, mm_to_cm, input_str)
    return result
