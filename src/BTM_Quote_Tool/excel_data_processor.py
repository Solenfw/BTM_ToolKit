import os
import re
import sys
import pandas as pd

os.system("")

CYAN = '\033[1;96m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[1;35m'
END = '\033[0m'

# data source
source_file = r"../../data/DMSP KLS MARTIN.xlsx"

sheet_dict = {}

def file_process(file_path: object) -> object:
    data_raw = pd.read_excel(file_path)
    data_raw['col_a_value'] = data_raw.iloc[:, 0].astype(str).str.strip().str.lower()  # Column A
    data_raw['col_b_value'] = data_raw.iloc[:, 1].astype(str).str.strip().str.lower()  # Column B
    data_raw['col_c_value'] = data_raw.iloc[:, 2].astype(str).str.strip().str.lower()  # Column C

    unique_counter = 0
    for row in data_raw.iloc[:].itertuples(index=False):
        col_a_value = row.col_a_value  
        col_b_value = row.col_b_value  
        col_c_value = row.col_c_value  

        if col_c_value in sheet_dict:
            sheet_dict[f"{unique_counter}-{col_c_value}"] = [col_b_value, col_a_value]
            unique_counter += 1
        else:
            sheet_dict[col_c_value] = [col_b_value, col_a_value]



def display(product : str, stats : list):
    descript = re.sub(r'(\d+)', r'\033[1;35m\1\033[0m', product)
    eng_descript = re.sub(r'(\d+)', r'\033[1;35m\1\033[0m', stats[0])
    code = stats[1]

    descript_width = 70
    eng_descript_width = 65
    code_width = 20
    print(f"_ {descript.ljust(descript_width)} "
          f"    {CYAN}{eng_descript.ljust(eng_descript_width)}{END} "
          f"    {YELLOW}{code.ljust(code_width)}{END}")


def all_exist(keys : list, check_string : str) -> bool:
    return all(key in check_string for key in keys)

def not_exist(words : list, target : str) -> bool:
    return not any(word in target for word in words)

def process_command():
    while True:
        try:
            command = int(input("Command (1 to start and 0 to terminate the program): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if command == 0:
            print("Terminating. . . ")
            sys.exit(0)

        elif command == 1:
            # prior report
            print("Report : ")
            print(f"Number of items Information acquired : {len(sheet_dict)}")
            print(f"Proceeding . . .")

            while True:
                our_options = {}
                # Step 1: Input significant keywords
                sigKeyString = input("\033[1;31mEnter sigKey(s): \033[0m")
                sigKey = [word for word in sigKeyString.strip().lower().split()]

                # step 2 : Exclude unwanted words
                excludeString = input("Exclude : ")
                exclude_words = [word for word in excludeString.strip().lower().split()]

                # Check for CODE matching - input special case
                code_pattern = r'\d{2}-\d{3}-\d{2}-\d{2}'
                if sigKeyString == 'cls' or sigKeyString == 'clear':
                    os.system('cls')
                elif re.fullmatch(code_pattern, sigKeyString):
                    for prd_descript, stats in sheet_dict.items():
                        if stats[1] == sigKeyString:
                            display(prd_descript, stats)
                            break
                else:
                    
                    # Step 3: Search for products containing all significant keywords
                    for prd_descript, stats in sheet_dict.items():
                        if all_exist(sigKey, prd_descript) and not_exist(exclude_words, prd_descript):
                            our_options[prd_descript] = stats

                    if not our_options:
                        print("No match found for sigKey(s).")
                        try:
                            command = int(input("Re-enter sigKey(s) (any key to re-enter, 0 to terminate): "))
                            if command == 0:
                                print("Terminating. . . ")
                                sys.exit(0)
                        except ValueError:
                            print("retry...")
                    else:

                        # Step 4: Ask for additional detail (optional)
                        detail = input("Detail (optional): ")
                        details = [e for e in detail.strip().lower().split()]
                        if not detail:
                            for prd_descript, stats in our_options.items():
                                display(prd_descript, stats)
                        else:
                            cleaned_options = {}
                            for prd_descript, stats in our_options.items():
                                if all_exist(details, stats[0]):
                                    cleaned_options[prd_descript] = stats
                            if cleaned_options:
                                for prd_descript, stats in cleaned_options.items():
                                    display(prd_descript, stats)
                            else:
                                print("No match found after details provided. ")
                                del cleaned_options
                    del our_options

        else:
            print("Invalid command. Try again!")



file_process(source_file)
if __name__ == '__main__':
    process_command()
