import regex
import csv
import os
import subprocess
import shlex
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .string_utilities import string_cleaner

console = Console()

class SupportUtils:

    @staticmethod
    def help():
        """Displays a user-friendly help message with command descriptions and examples."""

        console.print(Panel(
            "[bold cyan]Welcome to the BTM Quote Tool![/bold cyan]\n\nThis tool helps you search for medical products and manage quotes.",
            title="[bold green]BTM Quote Tool Manual[/bold green]",
            expand=False
        ))

        # General Commands Table
        general_table = Table(title="[bold]General Commands[/bold]", show_header=True, header_style="bold magenta")
        general_table.add_column("Command", style="dim", width=15)
        general_table.add_column("Description", style="bright_blue")
        general_table.add_column("Example", style="yellow")

        general_table.add_row("help", "Displays this help message.", "help")
        general_table.add_row("end", "Terminates the program.", "end")
        general_table.add_row("clear", "Clears the console screen.", "clear")
        general_table.add_row("refresh", "Reloads the product data from source files.", "refresh")

        console.print(general_table)

        # Search Commands Table
        search_table = Table(title="[bold]Search Commands[/bold]", show_header=True, header_style="bold magenta")
        search_table.add_column("Command", style="dim", width=15)
        search_table.add_column("Description", style="bright_blue")
        search_table.add_column("Example", style="yellow")

        search_table.add_row("sculap [keyword]", "Searches for an Aesculap product.", "sculap instrument")
        search_table.add_row("integra [keyword]", "Searches for an Integra product.", "integra forceps")
        search_table.add_row("search_by_code [KLS code]", "Searches for a product by its exact code. (for Aesculap just type directly).", "search_by_code 12-345-67-89")

        console.print(search_table)

        # Quote Management Commands Table
        quote_table = Table(title="[bold]Quote Management Commands[/bold]", show_header=True, header_style="bold magenta")
        quote_table.add_column("Command", style="dim", width=15)
        quote_table.add_column("Description", style="bright_blue")
        quote_table.add_column("Example", style="yellow")

        quote_table.add_row("load [code]", "Saves a product code to your selection.", "load 12-345-67-89")
        quote_table.add_row("pick [index]", "Picks a product from the search results by its index.", "pick 3")
        quote_table.add_row("check", "Displays all selected product codes. [ -c, -o flags to clear/open]", "check")
        quote_table.add_row("reference", "Shows the reference file content. [ -c, -o flags to clear/open]", "reference")

        console.print(quote_table)

        # Utility Commands Table
        utility_table = Table(title="[bold]Utility Commands[/bold]", show_header=True, header_style="bold magenta")
        utility_table.add_column("Command", style="dim", width=15)
        utility_table.add_column("Description", style="bright_blue")
        utility_table.add_column("Example", style="yellow")

        utility_table.add_row("inch [value]", "Converts a value from centimeters to inches.", "inch 10")
        utility_table.add_row("replace [old_code] [new_code]", "Replaces a code in your selection.", "replace 12-345-67-89 98-765-43-21")

        console.print(utility_table)


    @staticmethod
    def load(code: str):
        """Saves selected code to a file."""
        selected_code_file = "selected_code.txt"
        try:
            if not os.path.exists(selected_code_file):
                open(selected_code_file, 'w', encoding='utf-8').close()
            
            with open(selected_code_file, 'a', encoding='utf-8') as file:
                    file.write(code + "\n")
        except Exception as err:
            console.print(f"ERROR : {err}")
    

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
            console.print(f"ERROR : {err}. Please enter a valid number.")
        except IndexError as err:
            console.print(f"ERROR : {err}. Please enter a number between 1 and {len(dataset)}.")
        except Exception as err:
            console.print(f"ERROR : {err}")


    @staticmethod
    def check(data: dict[str, tuple[str, str]], flags: list[str] = None):
        """Checks the saved codes."""
        selected_code_file = "selected_code.txt"
        try:
            # arguments handling
            if '-c' in flags:
                open(selected_code_file, 'w', encoding='utf-8').close()
                console.print("Selected code file cleared.")
                return
            elif '-o' in flags:
                console.print("Opening selected code file...")
                cmd = "notepad ./selected_code.txt" if os.name == 'nt' else "micro ./selected_code.txt"
                subprocess.run(shlex.split(cmd))
                return
            
            # Ensure file exists
            if not os.path.exists(selected_code_file):
                open(selected_code_file, 'w', encoding='utf-8').close()

            # Read selected codes
            with open(selected_code_file, 'r', encoding='utf-8') as file:
                codes = file.read().splitlines()

            # Handle empty file
            if not codes:
                console.print("File Empty!")
                return

            # Display codes
            for index, code in enumerate(codes, start=1):
                matching_item = next(
                    (vietnamese for vietnamese, (_, original_code) in data.items() if original_code == code), "None"
                )
                if matching_item:
                    console.print(f"{index} _ [yellow]{code}[/yellow] _ [white]{matching_item}[/white]")
                else:
                    console.print(f"{index} _ {code}")

        except FileNotFoundError as err:
            console.print(f"ERROR: {err}")


    @staticmethod
    def reference(flags: list[str] = None):
        reference_file = 'reference.txt'
        selected_code_file = 'selected_code.txt'
        
        try:
            # arguments handling
            if '-c' in flags:
                open(reference_file, 'w', encoding='utf-8').close()
                console.print("Reference file cleared.")
                return
            elif '-o' in flags:
                console.print("Opening reference file...")
                cmd = "notepad ./reference.txt" if os.name == 'nt' else "micro ./reference.txt"
                subprocess.run(shlex.split(cmd))
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
                command = console.input("File is empty! Fill it up? (y): ").strip()
                if command == 'y':
                    console.print("Opening reference file for editing...")
                    cmd = "notepad ./reference.txt" if os.name == 'nt' else "micro ./reference.txt"
                    subprocess.run(shlex.split(cmd))
                return

            # Display relevant information
            if current_prd == 0:
                console.print(f"First item: {lines[0]}")
            elif current_prd < len(lines):
                console.print(f"{current_prd} _ {lines[current_prd - 1]} - {codes_avail[current_prd - 1]}")
                console.print(f"Next: {current_prd + 1} _ {lines[current_prd]}")
            else:
                console.print("All references have been used. Open reference file for more information.")

        except FileNotFoundError as err:
            console.print(f"ERROR: {err}")

    @staticmethod
    def all_keys_exist(keys: list, check_string: str) -> bool:
        """Returns True if all keys exist in the check string (case-insensitive)."""
        check_string_lower = check_string.lower()
        return all(key.lower() in check_string_lower for key in keys)


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
            console.print(f"Old code replaced.")
        except Exception as err:
            console.print(f"ERROR : {err}")

    @staticmethod
    def highlight_text(text: str, keywords: list[str], color: str = "yellow") -> str:
        """Highlights keywords in a given text using rich formatting."""
        if not keywords:
            return text
        
        highlighted_text = text
        for keyword in keywords:
            # Use regex to find and replace all occurrences of the keyword, case-insensitive
            # Wrap the matched keyword with rich color tags
            highlighted_text = regex.sub(
                f"({regex.escape(keyword)})",
                f"[{color}]\g<1>[/{color}]",
                highlighted_text,
                flags=regex.IGNORECASE
            )
        return highlighted_text


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
            console.print(f"Error processing Aesculap data: {e}")


    
    def search(self, keyword: str, dataset: dict):
        try:
            temporary = {}
            keyword_list = keyword.lower().split()
            for code, (descript, alternative) in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, descript):
                    temporary[code] = (descript, alternative)
            return temporary
        except Exception as e:
            console.print(f"Error searching Aesculap data: {e}")
    

    @staticmethod
    def display(tempo : dict[str, tuple[str, str]], keywords: list[str] = None):
        try:
            table = Table(title="Aesculap Products")
            table.add_column("Idx", justify="right", style="cyan", no_wrap=True)
            table.add_column("Code", style="magenta")
            table.add_column("Description", style="green")
            table.add_column("Alternative", style="yellow")

            for index, (code, (description, alternative)) in enumerate(tempo.items()):
                highlighted_description = SupportUtils.highlight_text(description, keywords)
                highlighted_alternative = SupportUtils.highlight_text(alternative, keywords)
                table.add_row(str(index + 1), code, highlighted_description, highlighted_alternative)

            console.print(table)
        except Exception as e:
            console.print(f"Error displaying Aesculap data: {e}")
        

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
            console.print(f"Error processing Integra data: {e}")
        return self.dataset


    def search(self, keyword: str, dataset : dict):
        try:
            keyword_list = keyword.strip().lower().split()
            for code, description in dataset.items():
                if SupportUtils.all_keys_exist(keyword_list, description):
                    highlighted_description = SupportUtils.highlight_text(description, keyword_list)
                    console.print(f"[magenta]{code}[/magenta]	{highlighted_description}")
        except Exception as e:
            console.print(f"Error searching Integra data: {e}")


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
            console.print(f"Error processing KLS data: {e}")


    @staticmethod
    def display(temporary: dict, keywords: list[str] = None):
        try:
            table = Table(title="KLS Products")
            table.add_column("Idx", justify="right", style="cyan", no_wrap=True)
            table.add_column("Vietnamese Description", style="green")
            table.add_column("English Description", style="cyan")
            table.add_column("Code", style="yellow")

            for index, (code, (eng_descript, vn_descript)) in enumerate(temporary.items()):
                highlighted_vn_descript = SupportUtils.highlight_text(vn_descript, keywords)
                highlighted_eng_descript = SupportUtils.highlight_text(eng_descript, keywords)
                table.add_row(str(index + 1), highlighted_vn_descript, highlighted_eng_descript, code)
            
            console.print(table)
            return [[index + 1, vn_descript, eng_descript, code] for index, (code, (eng_descript, vn_descript)) in enumerate(temporary.items())]
        except Exception as e:
            console.print(f"Error displaying KLS data: {e}")


    def SearchByCode(self, keyword: str, AesculapDataset: dict):
        try:
            if not self.dataset:
                console.print("The dataset is empty. Please process data before searching.")
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
                            console.print(f"Alternative AESCULAP code: [yellow]{aesculap_code}[/yellow]")
                            break  # Exit the loop early when a match is found
            
            # Display results or notify if no matches
            self.display(temporary, keywords=[keyword]) if temporary else console.print("No matching code found.")
        except Exception as e:
            console.print(f"Error searching KLS data: {e}")


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
            console.print(f"Error searching KLS data: {e}")        
