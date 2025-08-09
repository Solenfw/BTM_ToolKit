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
    def wrap_text(text_input, color_code, keywords=None, whole=False):
        # Ensure text_input is a string, as highlight might return non-string if not careful
        text = str(text_input)

        if whole:
            return f"{color_code}{text}{Color.END}"

        if keywords and isinstance(keywords, list) and len(keywords) > 0:
            processed_text = text
            for keyword in keywords:
                if not keyword:  # Skip empty keywords
                    continue
                # Escape keyword for regex to treat special characters literally
                # Use regex.IGNORECASE for case-insensitive matching
                # Apply color_code ONLY to the matched keyword
                processed_text = regex.sub(
                    rf'({regex.escape(str(keyword))})',
                    lambda match: f"{color_code}{match.group(1)}{Color.END}",
                    processed_text,
                    flags=regex.IGNORECASE  # Add case-insensitivity
                )
            return processed_text # Return text with only keywords colored
        else:
            # This is the original Path C: if no keywords, color non-digit/dot/space sequences.
            # You might want to reconsider if this is the desired fallback.
            # If text should remain uncolored if no keywords, then just 'return text'
            return regex.sub(r'([^\d\.\s]+)', lambda match: f"{color_code}{match.group(0)}{Color.END}", text)

    @staticmethod
    def highlight(text: str) -> str:
        """Highlights numbers in MAGENTA within the text."""
        # Ensure text is a string
        text_str = str(text)
        return regex.sub(r'(\d+(\.\d+)?)', lambda match: f"{Color.MAGENTA}{match.group(1)}{Color.END}", text_str)


class SupportUtils:

    @staticmethod
    def help():
        print(
            "\nCommands:\n"
            "1. 'end' to terminate the program.\n"
            "2. 'code' to display selected codes.\n"
            "3. 'clear code' to clear selected codes.\n"
            "4. 'open code' to open selected codes file.\n"
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
    def pick(idx: str, dataset : list[list]):
        index = int(idx)
        selected_code_file = "selected_code.txt"
        try:
            if not os.path.exists(selected_code_file):
                open(selected_code_file, 'w', encoding='utf-8').close()
            
            with open(selected_code_file, 'a', encoding='utf-8') as file:
                    code = dataset[index - 1][3]
                    code = regex.search(r'\d{2}-\d{3}-\d{2}-\d{2}', code).group(0)
                    file.write(code + "\n")
        except ValueError as err:
            print(f"ERROR : {err}. Please enter a valid number.")
        except IndexError as err:
            print(f"ERROR : {err}. Please enter a number between 1 and {len(dataset)}.")
        except Exception as err:
            print(f"ERROR : {err}")


    @staticmethod
    def check(data: dict[str, tuple[str, str]], mode: str = ''):
        """Checks the saved codes."""
        selected_code_file = "selected_code.txt"
        try:
            # clear file content
            if mode == 'clear code':
                with open(selected_code_file, 'w', encoding='utf-8') as file:
                    print("FILE cleared.")
                return
            
            # open file in notepad
            if mode == "open code":
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
                    (vietnamese for vietnamese, (_, original_code) in data.items() if original_code == code), "None"
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
                command = input("File is empty! Fill it up? (y): ").strip()
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
                    code = str(row[0]).strip()
                    description = string_cleaner(row[1]) or "No description"
                    alternative = str(row[2]).strip()
                    self.dataset[code] = (description, alternative)
            return self.dataset
        except Exception as e:
            print(f"Error processing Aesculap data: {e}")


    
    def search(self, keyword: str, dataset: dict):
        try:
            temporary = {}
            keyword_list = keyword.split()
            for code, (descript, alternative) in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, descript):
                    temporary[code] = (descript, alternative)
            return temporary
        except Exception as e:
            print(f"Error searching Aesculap data: {e}")
    

    @staticmethod
    def display(tempo : dict[str, tuple[str, str]], keywords: list[str] = None):
        try:
            initial_data = [
                [
                    index + 1,  # Index of the code
                    Color.wrap_text(code, Color.CYAN, whole=True),  # Highlight and colorize Code
                    Color.wrap_text(description, Color.GREEN, keywords),  # Highlight and colorize Description
                    Color.wrap_text(alternative, Color.YELLOW, None, True)  # Colorize the Alternative
                ]
                for index, (code, (description, alternative)) in enumerate(tempo.items())
            ]
            # Define the headers for the table
            headers = ['Idx','Code', 'Description', 'Alternative']
            print(tabulate(initial_data, headers=headers, tablefmt="fancy_grid"))
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


    def search(self, keyword: str, dataset : dict):
        try:
            keyword_list = keyword.strip().lower().split()
            for code, description in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, description):
                    print(f"{Color.wrap_text(code, Color.CYAN, None, True)}\t{Color.highlight(description)}")
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
    def display(temporary: dict, keywords: list[str] = None):
        try:
            initial_data = [
                 [
                    index + 1,  # Index of the code
                    Color.wrap_text(vn_descript, Color.GREEN, keywords),  # Highlight and colorize Vietnamese Description
                    Color.wrap_text(eng_descript, Color.CYAN, keywords),  # Highlight and colorize English Description
                    Color.wrap_text(code, Color.YELLOW, keywords, whole=True)  # Colorize the Code
                ]
                for index, (code, (eng_descript, vn_descript)) in enumerate(temporary.items())
            ]
            
            headers = ['Idx',"Vietnamese Description", "English Description", "Code"]
            print(tabulate(initial_data, headers=headers, tablefmt="fancy_grid"))
            return initial_data
        except Exception as e:
            print(f"Error displaying KLS data: {e}")


    def SearchByCode(self, keyword: str, AesculapDataset: dict):
        try:
            if not self.dataset:
                print("The dataset is empty. Please process data before searching.")
                return
            
            temporary = {}
            keyword = keyword.strip().lower()  # Normalize keyword for case-insensitive matching

            # Search for the keyword in self.dataset
            for code, info in self.dataset.items():
                if code.lower() == keyword:
                    temporary[code] = info

                    # Search for alternatives in AesculapDataset
                    for aesculap_code, information in AesculapDataset.items():
                        if len(information) > 1 and information[1].lower() == keyword:
                            print(f"Alternative AESCULAP code: {Color.wrap_text(aesculap_code, Color.YELLOW, None, True)}")
                            break  # Exit the loop early when a match is found
            
            # Display results or notify if no matches
            self.display(temporary, keywords=[keyword]) if temporary else print("No matching code found.")
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
