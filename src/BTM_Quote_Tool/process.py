import regex
import csv
import os
from pathlib import Path
from tabulate import tabulate
from .string_utilities import string_cleaner


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
        return regex.sub(r'([^\d\.\s]+)', lambda match: f"{color}{match.group(0)}{Color.END}", text)
    
    @staticmethod
    def highlight(text: str) -> str:
        """Highlights numbers in MAGENTA within the text while keeping other text in color."""
        return regex.sub(r'(\d+)', lambda match: f"{Color.MAGENTA}{match.group(0)}{Color.END}", text)


class SupportUtils:

    @staticmethod
    def help():
        print(
            "\nCommands:\n"
            "1. 'end' to terminate the program.\n"
            "2. 'check' to display selected codes.\n"
            "3. 'clear check' to clear selected codes.\n"
            "4. 'open check' to open selected codes file.\n"
            "5. 'clear rf' to clear reference file.\n"
            "6. 'open rf' to open reference file.\n"
            "7. 'replace' to replace a code.\n"
            "8. 'load' to save a code.\n"
            "9. put 'sculap' at the end to search for Aesculap code.\n"
            "10. put 'integra' at the end to search for Integra code.\n"
            "11. put 'inch' at the end to convert cm to inch.\n"
            "12. put 'refresh' to reload the data.\n"
            "13. put 'help' to display this message."
        )


    @staticmethod
    def save(code: str):
        """Saves selected code to a file."""
        selected_code_file = "selected_code.txt"
        try:
            if not os.path.exists(selected_code_file):
                open(selected_code_file, 'w', encoding='utf-8').close()
            
            with open(selected_code_file, 'a', encoding='utf-8') as file:
                    file.write(code + "\n")
        except Exception as err:
            print(f"ERROR : {err}")

    @staticmethod
    def check(data: dict[str, tuple[str, str]], mode: str = ''):
        """Checks the saved codes."""
        selected_code_file = "selected_code.txt"
        try:
            # clear file content
            if mode == 'clear check':
                with open(selected_code_file, 'w', encoding='utf-8') as file:
                    print("FILE cleared.")
                return
            
            # open file in notepad
            if mode == "open check":
                os.system("notepad ./selected_code.txt")
                return

            # Ensure file exists
            if not os.path.exists(selected_code_file):
                open(selected_code_file, 'w', encoding='utf-8').close()

            # Read selected codes
            with open(selected_code_file, 'r', encoding='utf-8') as file:
                codes = file.read().splitlines()

            # Handle empty file
            if not codes:
                print("File Empty!")
                return

            # Display codes
            for index, code in enumerate(codes, start=1):
                matching_item = next(
                    (vietnamese for vietnamese, (_, original_code) in data.items() if original_code == code), None
                )
                if matching_item:
                    print(f"{index} _ {Color.wrap_text(code, Color.YELLOW)} _ {Color.wrap_text(matching_item, Color.WHITE)}")
                else:
                    print(f"{index} _ {code}")

        except FileNotFoundError as err:
            print(f"ERROR: {err}")


    @staticmethod
    def reference(mode: str = ""):
        reference_file = 'reference.txt'
        selected_code_file = 'selected_code.txt'
        
        try:
            # Clear reference file content
            if mode == 'clear rf':
                with open(reference_file, 'w', encoding='utf-8') as file:
                    print("Reference cleared.")
                return

            # Open reference file in notepad
            if mode == 'open rf':
                os.system("notepad ./reference.txt")
                return

            # Ensure both files exist
            for file_name in [reference_file, selected_code_file]:
                if not os.path.exists(file_name):
                    open(file_name, 'w', encoding='utf-8').close()

            # Read contents of files
            with open(reference_file, 'r', encoding='utf-8') as ref_file:
                lines = ref_file.read().splitlines()
            with open(selected_code_file, 'r', encoding='utf-8') as code_file:
                codes_avail = code_file.read().splitlines()

            current_prd = len(codes_avail)

            # Handle empty reference file
            if not lines:
                command = input("File is empty! Fill it up? (y): ").strip().upper()
                if command == 'y':
                    print("Opening reference file for editing...")
                    os.system("notepad ./reference.txt")
                return

            # Display relevant information
            if current_prd == 0:
                print(f"First item: {lines[0]}")
            elif current_prd < len(lines):
                print(f"{current_prd} _ {lines[current_prd - 1]} - {codes_avail[current_prd - 1]}")
                print(f"Next: {current_prd + 1} _ {lines[current_prd]}")
            else:
                print("All references have been used. Open reference file for more information.")

        except FileNotFoundError as err:
            print(f"ERROR: {err}")


    @staticmethod
    def all_keys_exist(keys: list, check_string: str) -> bool:
        """Returns True if all keys exist in the check string."""
        return all(key in check_string for key in keys)


    @staticmethod
    def replace(old_code: str, new_code: str):
        selected_code_file = 'selected_code.txt'
        try:
            with open(selected_code_file, 'r', encoding='utf-8') as file:
                codes = file.readlines()
            updated_codes = [
                line.replace(old_code, new_code) if old_code in line else line 
                for line in codes
            ]
            with open(selected_code_file, 'w', encoding='utf-8') as file:
                file.writelines(updated_codes)
            print(f"Old code replaced.")
        except Exception as err:
            print(f"ERROR : {err}")


class AesculapUtils:
    def __init__(self):
        self.dataset = {}
    
    def DataProcess(self, file_path: Path) -> dict:
        """Processes Aesculap CSV file into a dictionary."""
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for row in csv_reader:
                    description = string_cleaner(str(row[1]).strip().lower() or "none")
                    code = str(row[1]).strip()
                    alternative = str(row[2]).strip()
                    self.dataset[code] = (description, alternative)
            return self.dataset
        except Exception as e:
            print(f"Error processing Aesculap data: {e}")


    
    def search(self, keyword: str, dataset: dict):
        try:
            keyword_list = keyword.strip().lower().split()
            for code, (descript, alternative) in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, descript):
                    descript = SupportUtils.highlight_numbers(descript)
                    self.display(code, (descript, alternative))
        except Exception as e:
            print(f"Error searching Aesculap data: {e}")
    

    @staticmethod
    def display(code: str, info: tuple[str, str]):
        try:
            description = SupportUtils.highlight_numbers(info[0])
            alternative = SupportUtils.highlight_numbers(info[1])
            data = [
                [description, alternative, code]  # One row with the columns
            ]
            # Define the headers for the table
            headers = ["Description", "Alternative", "Code"]
            # Use tabulate to display the data in table format
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        except Exception as e:
            print(f"Error displaying Aesculap data: {e}")
        

class IntegraUtils:
    def __init__(self):
        self.dataset = {}

    def DataProcess(self, file_path: Path) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for row in csv_reader:
                    code = row[0]
                    description = regex.sub(r',', ' ', str(row[1]).strip().lower())
                    self.dataset[code] = description
        except Exception as e:
            print(f"Error processing Integra data: {e}")
        return self.dataset


    def search(keyword: str, dataset : dict):
        try:
            keyword_list = keyword.strip().lower().split()
            for code, description in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, description):
                    print(f"{Color.wrap_text(code, Color.CYAN)}\t{SupportUtils.highlight_numbers(description)}")
        except Exception as e:
            print(f"Error searching Integra data: {e}")


class KLSUtils:
    def __init__(self):
        self.dataset = {}

    def DataProcess(self, file_path: Path) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)

                for row in csv_reader:
                    code = row[0].strip()
                    eng_descript = string_cleaner(row[1])
                    vn_descript = string_cleaner(row[2])

                    self.dataset[code] = (eng_descript, vn_descript)
            return self.dataset
        except Exception as e:
            print(f"Error processing KLS data: {e}")


    @staticmethod
    def display(temporary: dict):
        try:
            data = [
                [
                    Color.wrap_text(Color.highlight(vn_descript), Color.GREEN),  # Highlight and colorize Vietnamese Description
                    Color.wrap_text(Color.highlight(eng_descript), Color.CYAN),  # Highlight and colorize English Description
                    Color.wrap_text(code, Color.YELLOW)  # Colorize the Code
                ]
                for code, (eng_descript, vn_descript) in temporary.items()
            ]
            
            headers = ["Vietnamese Description", "English Description", "Code"]
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        except Exception as e:
            print(f"Error displaying KLS data: {e}")


    def SeachByCode(self, keyword: str, AesculapDataset: dict):
        try:
            temporary = {}
            keyword = keyword.strip()
            for code, info in self.dataset.items():
                if code == keyword:
                    temporary[code] = info
                    if self.dataset:
                        for AesculapCode, information in AesculapDataset.items():
                            if information[1] == keyword:
                                print(f"Alternative AESCULAP code: {Color.wrap_text(AesculapCode, Color.YELLOW)}")
            self.display(temporary)
        except Exception as e:
            print(f"Error searching KLS data: {e}")


    def search(self, keyword: str) -> dict:
        try:
            matching_products = {}
            keyword_list = keyword.strip().lower().split()

            for code, info in self.dataset.items():
                total_descript = info[0] + " " + info[1]
                if SupportUtils.all_keys_exist(keyword_list, total_descript):
                    matching_products[code] = info
            return matching_products
        except Exception as e:
            print(f"Error searching KLS data: {e}")        
