import regex
import csv
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from BTM_Quote_Tool.string_utilities import string_cleaner
from BTM_Quote_Tool.config import data_processor, load_config


# loading up data
config = load_config()
source_file = Path(config['csv_source']['kls_product_csv'])
source_for_aesculap = Path(config['csv_source']['aesculap_product_csv'])
source_for_integra = Path(config['csv_source']['integra_product_csv'])

os.system("")
class Color:
    CYAN = '\033[1;96m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    RED = '\033[1;31m'
    END = '\033[0m'
    GREEN = '\033[1;92m'
    WHITE = '\033[37m'
    
    @staticmethod
    def wrap_text(text, color):
        return f"{color}{text}{Color.END}"

class SupportUtils:
    @staticmethod
    def save_up(code: str):
        """Saves selected code to a file."""
        with open("selected_code.txt", 'a', encoding='utf-8') as file:
            actual_code = regex.search(r'\d{2}-\d{3}-\d{2}-\d{2}', code)
            if actual_code:
                file.write(actual_code.group() + "\n")
            else:
                file.write(code + "\n")

    @staticmethod
    def check_up(data : dict[str, (str, str)], mode : str = ''):
        """Checks the saved codes."""
        try:
            if mode == 'clear check':
                with open("selected_code.txt", 'w', encoding='utf-8') as file:
                    print("FILE cleared.")
                    pass
            with open("selected_code.txt", 'r', encoding='utf-8') as file:
                codes = file.read().splitlines()
            if len(codes) >= 1:
                for index, code in enumerate(codes):
                        flag = False
                        for vietnamese, (english, original_code) in data.items():
                            if original_code == code:
                                print(f"{index+1} _ {Color.wrap_text(code, Color.YELLOW)} _ {Color.wrap_text(vietnamese, Color.WHITE)}")
                                flag = True
                        else:
                            if not flag:
                                print(f"{index+1} _ {code}")
            else: 
                print("File Empty!")
        except Exception as err:
            print(f"ERROR : {err}")

    @staticmethod
    def get_reference(mode : str = ""):
        try:
            if mode == 'clear rf':
                with open ('reference.txt', 'w', encoding='utf-8') as file:
                    print("Reference cleared.")
                    pass
            
            with open ('reference.txt', 'r', encoding='utf-8') as file, open ('selected_code.txt', 'r', encoding='utf-8') as file2:
                lines = file.read().splitlines()
                codes_avail = file2.read().splitlines()
                current_prd = len(codes_avail)
                if not lines:
                    command = input("File Empty! Fill up ? (Y) : ")
                    if command == 'Y':
                        os.system("notepad ./reference.txt")
                if (len(codes_avail) == 0): 
                    print(f"First item : {lines[0]}")
                else:
                    print(f"{len(codes_avail)} _ {lines[current_prd - 1]} - {codes_avail[current_prd - 1]}") # zero-indexed
                    print(f"Next :{len(codes_avail)+1} _ {lines[current_prd]}")
        except Exception as err:
            print(f"ERROR : {err}")


    @staticmethod
    def highlight_numbers(text: str, color: str, highlight_color: str) -> str:
        """Highlights numbers within the text while keeping other text in color."""
        return regex.sub(r'(\d+)', lambda match: f"{highlight_color}{match.group(0)}{color}", text)

    @staticmethod
    def all_keys_exist(keys: list, check_string: str) -> bool:
        """Returns True if all keys exist in the check string."""
        return all(key in check_string for key in keys)


    
    @staticmethod
    def replace_code(old_code: str, new_code: str):
        try:
            with open('selected_code.txt', 'r', encoding='utf-8') as file:
                codes = file.readlines()
            updated_codes = [
                line.replace(old_code, new_code) if old_code in line else line 
                for line in codes
            ]
            with open('selected_code.txt', 'w', encoding='utf-8') as file:
                file.writelines(updated_codes)
            print(f"Old code replaced.")
        except Exception as err:
                    print(f"ERROR : {err}")
            

class AesculapUtils:
    def __init__(self):
        self.aesculap_data = {}
    
    def data_processing_for_aesculap(self, file_path: Path) -> dict:
        """Processes Aesculap CSV file into a dictionary."""
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                description = string_cleaner(str(row[0]).strip().lower() or "none")
                aesculap_code = str(row[1]).strip()
                kls_code = str(row[2]) or "none"
                self.aesculap_data[aesculap_code] = (description, kls_code)
        if len(self.aesculap_data) > 0:
            print(f"Successfully loaded Aesculap's Data.")
        return self.aesculap_data

    @staticmethod
    def get_information_from_aesculap(keyword: str, aesculap_data: dict):
        keyword = keyword.replace('.', '')
        """Performs the product search based on significant keywords and exclusion."""
        keyword_list = keyword.strip().lower().split()[:-1]
        for aesculap_code, information in aesculap_data.items():
            desription = information[0]
            alternative = information[1]
            if SupportUtils.all_keys_exist(keyword_list, desription):
                desription = SupportUtils.highlight_numbers(desription, Color.GREEN, Color.YELLOW)
                print(f"_ {Color.GREEN}{aesculap_code.ljust(len(aesculap_code) + 5)}{Color.END}    "
                      f"{Color.CYAN}{desription.ljust(len(desription) + 5)}{Color.END}    "
                      f"{Color.YELLOW}{alternative}{Color.END}")


class IntegraUtils:
    def __init__(self):
        self.integra_data = {}

    def data_processing_for_integra(self, file_path: Path) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for row in csv_reader:
                    code = row[0]
                    description = regex.sub(r',', ' ', str(row[1]).strip().lower())
                    self.integra_data[code] = description
        except Exception as e:
            print(f"Error processing Integra data: {e}")
        if len(self.integra_data) > 0:
            print(f"Successfully loaded Integra's Data.")
        return self.integra_data

    @staticmethod
    def search_integra(keyword: str, integra_data : dict):
        flag = False
        keyword_list = keyword.strip().lower().split()
        for code, description in integra_data.items():
            if SupportUtils.all_keys_exist(keyword_list, description):
                flag = True
                print(f"{Color.CYAN}{code}{Color.END}"
                      f"     {SupportUtils.highlight_numbers(description, Color.WHITE, Color.MAGENTA)}")
        if not flag:
            print("No match acquired for the keyword.")

class KLSUtils:
    def __init__(self):
        self.kls_data = {}

    @staticmethod
    def display(product: str, stats: tuple):
        """Displays product information with formatted output."""
        descript = SupportUtils.highlight_numbers(product, Color.GREEN, Color.MAGENTA)
        eng_descript = SupportUtils.highlight_numbers(stats[0], Color.GREEN, Color.MAGENTA)
        code = stats[1]
        print(f"_ {Color.GREEN}{descript.ljust(len(descript) + 5)}{Color.END}    "
              f"{Color.CYAN}{eng_descript.ljust(len(eng_descript) + 5)}{Color.END}    "
              f"{Color.YELLOW}{code}{Color.END}")

    @staticmethod
    def search_by_code(keyword: str, kls_data : dict, aesculap_data : dict = None):
        """Searches for products by matching the code exactly."""
        keyword = keyword.strip()
        for prd_descript, stats in kls_data.items():
            if stats[1] == keyword:
                KLSUtils.display(prd_descript, stats)
                if aesculap_data:
                    for aesculap_code, information in aesculap_data.items():
                        if information[1] == keyword:
                            print(f"Alternative AESCULAP code: {Color.CYAN}{aesculap_code}{Color.END}")
                return True
        return False

    @staticmethod
    def product_search(keyword: str, kls_data : dict) -> dict:
        """Searches for products based on significant keywords."""
        matching_products = {}
        keyword_list = keyword.strip().lower().split()

        for prd_descript, stats in kls_data.items():
            total_descript = prd_descript + " " + stats[0]
            if SupportUtils.all_keys_exist(keyword_list, total_descript):
                matching_products[prd_descript] = stats
        return matching_products


def process_command():
    # preloading all .txt resources.
    with open("source_text/KLS_PDF_text.txt", "r", encoding='utf-8') as file:
        kls_catalog = file.read().lower()
    with open("source_text/INTEGRA_PDF.txt", "r", encoding='utf-8') as file:
        integra_catalog = file.read().lower()
    with open("source_text/AESCULAP_PDF.txt", "r", encoding='utf-8') as file:
        aesculap_catalog = file.read().lower()

    # pre-process raw data for Aesculap, KLS and Integra (csv)
    aesculap_obj = AesculapUtils()
    aesculap_data = aesculap_obj.data_processing_for_aesculap(source_for_aesculap)
    integra_obj = IntegraUtils()
    integra_data = integra_obj.data_processing_for_integra(source_for_integra)
    kls_data = data_processor(source_file)

    color = Color()

    # main action
    while True:
        command = input("Command (1 to start, 0 to terminate): ").strip()

        if command == '0':
            print("Terminating. . . ")
            sys.exit(0)

        if command == '1':
            print(f"Report:\nNumber of items Information acquired: {len(kls_data)}\nProceeding. . .")

            while True:
                keyword = input(color.wrap_text("Enter sigKey(s): ", Color.RED))
                keyword = string_cleaner(keyword)

                if keyword.lower() == 'end':
                    print("Terminating. . . ")
                    sys.exit(0)

                if keyword.endswith('rf'):
                    SupportUtils.get_reference(keyword)
                    continue

                if keyword.endswith('check'):
                    SupportUtils.check_up(kls_data, keyword)
                    continue
                
                if keyword.endswith('inch'):
                    value_in_cm = int(regex.match(r'\d+', keyword).group())
                    print(value_in_cm * 2.54)
                    continue

                if keyword.endswith('replace'):
                    try:
                        match = regex.findall(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword)
                        old_code = match[0]
                        new_code = match[1]
                        SupportUtils.replace_code(old_code, new_code)
                        continue
                    except Exception as err:
                        print(f"ERROR : {err}")
                        continue

                if keyword.endswith('load'):
                    SupportUtils.save_up(keyword)
                    print("Done saved up code.")
                    continue

                if keyword.endswith('sculap'):
                    AesculapUtils.get_information_from_aesculap(keyword, aesculap_data)
                    continue

                if keyword.endswith('integra'):
                    product = keyword.replace('integra', '')
                    IntegraUtils.search_integra(product, integra_data)
                    continue

                if keyword == 'refresh':
                    kls_data = data_processor(source_file)
                    print("Data has been refreshed. Continuing . . ")
                    continue

                # Clear screen or check by code if entered
                if keyword.endswith('clear') or keyword.endswith('cls'):
                    os.system('cls')
                    continue

                if regex.fullmatch(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword):
                    if KLSUtils.search_by_code(keyword, kls_data, aesculap_data):
                        continue

                matching_products = KLSUtils.product_search(keyword, kls_data)

                if not matching_products:
                    # keyword is an item of Aesculap 
                    if keyword.upper().strip() in aesculap_data.keys():
                            actual_key = keyword.upper().strip()
                            KLSUtils.display(actual_key, aesculap_data[actual_key])
                    
                    # keyword is an item of Integra
                    elif keyword.upper() in integra_data.keys():
                        code = keyword.upper()
                        description = integra_data[code]
                        print(f"{Color.CYAN}{code}{Color.END}    "
                              f"{SupportUtils.highlight_numbers(description, Color.YELLOW, Color.MAGENTA)}")

                    # Search for keyword among the .txt resoures from Catalogs.
                    elif keyword in kls_catalog:
                        print("Look up the KLS Catalog.")
                    elif keyword in integra_catalog:
                        print("Look up the INTEGRA catalog.")
                    elif keyword in aesculap_catalog:
                        print("Look up the AESCULAP catalog.")
                    else:
                        print("No match found for sigKey(s).")
                        if input("re-enter sigKey(s) or 0 to terminate: ") == '0':
                            sys.exit(0)
                else:
                    if len(matching_products.keys()) > 300:
                        confirm_input = input("More than 300 results. continue? (Y) ")
                        if confirm_input == 'Y':
                            for prd_descript, stats in matching_products.items():
                                KLSUtils.display(prd_descript, stats)
                    else:
                        for prd_descript, stats in matching_products.items():
                                KLSUtils.display(prd_descript, stats)


if __name__ == '__main__':
    print("Source file : ",source_file)
    process_command()