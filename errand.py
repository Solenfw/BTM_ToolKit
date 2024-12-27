import csv
import re
import os
from pathlib import Path
import pdfplumber
from rapidfuzz import fuzz
from myscripts.script import PDFUtils
from BTM_Quote_Tool.config import load_config
config = load_config()
kls_source_file = Path(config['csv_source']['kls_product_csv'])

os.system("")
class Color:
    CYAN = '/033[1;96m'
    YELLOW = '/033[1;33m'
    MAGENTA = '/033[1;35m'
    RED = '/033[1;31m'
    END = '/033[0m'
    GREEN = '/033[1;92m'
    
    @staticmethod
    def wrap_text(text, color):
        return f"{color}{text}{Color.END}"

def quick_convert():
    with open('whatever.txt', 'r', encoding='utf-8') as what, open('set_1.txt', 'w', encoding='utf-8') as set_1, open('result.txt', 'w', encoding='utf-8') as out:
        lines = what.read().splitlines()
        for line in lines:
            match = re.match(r'(.*): (\d+) (.*)', line)
            quantity = match.group(2)
            measure_unit = match.group(3).capitalize()
            product = match.group(1)
            set_1.write(quantity + "\n")
            out.write(product + "\n")

def process_duplicates():
    with open(kls_source_file, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = list(csvreader)
        
        duplicates = {}

        for index, row in enumerate(rows[1:]):
            if index == 3000:
                break
            elif index > 2000:
                code = row[0]
                english = row[1]
                vietnamese = row[2]

                if vietnamese not in duplicates:
                    duplicates[vietnamese] = [(index, code, english)]  
                else:
                    duplicates[vietnamese].append((index, code, english))  

    with open('whatever.txt', 'w', encoding='utf-8') as file:
        for vietnamese, duplicate_descripts in duplicates.items():
            if len(duplicate_descripts) >= 2:
                file.write(f"Vn: {vietnamese}/n")
                for dup in duplicate_descripts:
                    file.write(f"/t{'  '.join([str(item) for item in dup])}/n")  

def add_from_first_comma(inputString : str, text_to_add : str) -> str:
    if text_to_add in inputString:
        return inputString
    firstComma = inputString.find(',')
    newString = ''
    if firstComma != -1:
        newString = inputString[:firstComma] + f", {text_to_add}," + inputString[firstComma + 1:]
    else:
        newString = inputString + " " + text_to_add
    return re.sub(r'/s+', ' ', newString)

def modification():
    file_path = './whatever.txt'
    result_path = './result.txt'
    mode = input("action: ")
    if mode == 'replace':
        try:
            # Open the input file in Notepad and wait for it to close
            os.system(f'notepad {file_path}')

            # Extract codes to modify from the input file
            with open(file_path, 'r', encoding='utf-8') as codeInput:
                text = codeInput.read()
                codes_to_modify = [code.strip() for code in re.findall(r'\d{2}-\d{3}-\d{2}-\d{2}', text)]

            # Process the source CSV and write to the result file
            with open(kls_source_file, 'r', encoding='utf-8') as csvfile, open(result_path, 'w', encoding='utf-8') as output:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    code = row[0].strip()
                    vietnamese = row[2].strip()

                    if code in codes_to_modify:
                        output.write(f"{code}_{vietnamese}_\n")

            # Allow the user to edit the result file in Notepad
            os.system(f"notepad {result_path}")

            # Read modifications made by the user
            with open(result_path, 'r', encoding='utf-8') as output:
                raw_data = {
                    line.split("_")[0]: (line.split("_")[2].strip(), line.split("_")[3].strip())
                    for line in output
                }

            # Update the source CSV with modified Vietnamese descriptions
            updated_rows = []
            with open(kls_source_file, 'r', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    code = row[0].strip()
                    vietnamese = row[2].strip()

                    if code in raw_data.keys():
                        original_data = raw_data[code][0]
                        text_to_repalce_with = raw_data[code][1]
                        vietnamese = vietnamese.replace(original_data, text_to_repalce_with)

                    row[2] = vietnamese
                    updated_rows.append(row)

            # Write updated rows back to the CSV file
            if raw_data:
                with open(kls_source_file, 'w', encoding='utf-8', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(updated_rows)
            else:
                print("No data to be modified. Abort!!!")
        except Exception as err:
            print(f"ERROR occured : {err}")
    else:
        try:
            # Open the input file in Notepad and wait for it to close
            os.system(f'notepad {file_path}')

            # Extract codes to modify from the input file
            with open(file_path, 'r', encoding='utf-8') as codeInput:
                text = codeInput.read()
                codes_to_modify = [code.strip() for code in re.findall(r'\d{2}-\d{3}-\d{2}-\d{2}', text)]

            # Process the source CSV and write to the result file
            with open(kls_source_file, 'r', encoding='utf-8') as csvfile, open(result_path, 'w', encoding='utf-8') as output:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    code = row[0].strip()
                    vietnamese = row[2].strip()

                    if code in codes_to_modify:
                        output.write(f"{code}_{vietnamese}_\n")

            # Allow the user to edit the result file in Notepad
            os.system(f"notepad {result_path}")

            # Read modifications made by the user
            with open(result_path, 'r', encoding='utf-8') as output:
                raw_data = {
                    line.split("_")[0]: line.split("_")[2].strip()
                    for line in output
                }

            # Update the source CSV with modified Vietnamese descriptions
            updated_rows = []
            with open(kls_source_file, 'r', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    code = row[0].strip()
                    vietnamese = row[2].strip()

                    if code in raw_data.keys():
                        text_to_add = raw_data[code]
                        vietnamese = add_from_first_comma(vietnamese, text_to_add)

                    row[2] = vietnamese
                    updated_rows.append(row)

            # Write updated rows back to the CSV file
            if raw_data:
                with open(kls_source_file, 'w', encoding='utf-8', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(updated_rows)
            else:
                print("No data to be modified. Abort!!!")
        except Exception as err:
            print(f"ERROR occured : {err}")
    print("Modification completed.")

def header_getter():
    pdf_source = r'C:/Users/mimoz/OneDrive/Desktop/DOCUMENTS/BTM/KLS_MARTIN/CATALOUGE/KLS_Martin_Catalog.pdf'
    try: 
        product_line_file = Path(config['raw_text']['productlines'])
        with pdfplumber.open(pdf_source) as pdf_file, open (product_line_file, 'w', encoding='utf-8') as out:
            productlines = set()
            for index, page in enumerate(pdf_file.pages[5:]):
                if index == 978:
                    break
                header_box = (
                    0,                       # x0: Top-left corner (horizontal start)
                    0,                       # y0: Top-left corner (vertical start)
                    page.width,              # x1: decide box width counting from the left
                    page.height * 0.2        # y1: 20% down from the top
                )
                words_in_bbox = page.within_bbox(header_box).extract_text()
                words_in_second_rw = ''
                if words_in_bbox:
                    lines = words_in_bbox.split("\n")
                    if len(lines) > 1:
                        words_in_second_rw = lines[1]
                if words_in_second_rw : productlines.add(words_in_second_rw.strip())
            for product in productlines:
                out.write(product + "\n\n")
    except Exception as err:
        print(f"Conflict occurred : {err}")

    
def main():
    pass





if __name__ == '__main__':
    # quick_convert()
    # header_getter()
    modification()
    # main()

    print(f"Done!!")


