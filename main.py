import regex
import csv
import sys
import os
from pathlib import Path

os.system("")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Determine the base directory
if getattr(sys, 'frozen', False):
    base_dir = os.path.abspath(os.path.join(sys._MEIPASS, "..", "..", ".."))  # Temporary folder where PyInstaller extracts files
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))

# Ensure correct paths
sys.path.insert(0, os.path.join(base_dir, "src"))

# Set the correct path for config.json
config_path = os.path.join(base_dir, "config.json")

# Import custom module
from BTM_Quote_Tool import load_config, string_cleaner, AesculapUtils, IntegraUtils, KLSUtils, Color, SupportUtils

# loading up data
config = load_config(config_path)
MartinSourceFile = Path(config['csv_source']['kls_product_csv'])
AesculapSourceFile = Path(config['csv_source']['aesculap_product_csv'])
IntegraSourceFile = Path(config['csv_source']['integra_product_csv'])

MartinSourceText = Path(config['source_text']['kls_text'])
IntegraSourceText = Path(config['source_text']['integra_text'])
AesculapSourceText = Path(config['source_text']['aesculap_text'])


# Main function
def main():
    # preloading all .txt resources.
    with open(MartinSourceText, "r", encoding='utf-8') as file:
        MartinCatalog = file.read().lower()
    with open(IntegraSourceText, "r", encoding='utf-8') as file:
        IntegraCatalog = file.read().lower()
    with open(AesculapSourceText, "r", encoding='utf-8') as file:
        AesculapCatalog = file.read().lower()

    # Pre-process raw data for Aesculap, KLS, and Integra (csv)
    objects = {
        'Aesculap': AesculapUtils(),
        'Integra': IntegraUtils(),
        'Martin': KLSUtils()
    }

    AesculapDataset = objects['Aesculap'].DataProcess(AesculapSourceFile)
    IntegraDataset = objects['Integra'].DataProcess(IntegraSourceFile)
    MartinDataset = objects['Martin'].DataProcess(MartinSourceFile)

        # main action
    def handle_help():
        SupportUtils.help()

    def handle_terminate():
        print("Terminating. . . ")
        sys.exit(0)

    def handle_reference(keyword):
        SupportUtils.reference(keyword)

    def handle_check(keyword):
        SupportUtils.check(MartinDataset, keyword)

    def handle_inch(keyword):
        value_in_cm = int(regex.match(r'\d+', keyword).group())
        print(value_in_cm * 2.54)

    def handle_replace(keyword):
        try:
            match = regex.findall(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword)
            old_code = match[0]
            new_code = match[1]
            SupportUtils.replace(old_code, new_code)
        except Exception as err:
            print(f"ERROR : {err}")

    def handle_load(keyword):
        keyword = keyword.replace('load', '').strip()
        SupportUtils.save(keyword)
        print("Product's code has been loaded.")

    def handle_sculap(keyword):
        keyword = keyword.replace('sculap', '').strip()
        temp = objects['Aesculap'].search(keyword, AesculapDataset)
        if temp:
            objects['Aesculap'].display(temp)

    def handle_integra(keyword):
        product = keyword.replace('integra', '').strip()
        objects['Integra'].search(product, IntegraDataset)

    def handle_refresh():
        global MartinDataset
        MartinDataset = objects['Martin'].DataProcess(MartinSourceFile)
        print("Data has been updated. Continuing . . ")

    def handle_clear():
        os.system('cls')

    def handle_search_by_code(keyword):
        return objects['Martin'].SearchByCode(keyword, AesculapDataset)

    def handle_search(keyword):
        matching_products = objects['Martin'].search(keyword)
        if not matching_products:
            keyword_upper = keyword.upper().strip()
            if keyword_upper in AesculapDataset.keys():
                temp = {keyword_upper: AesculapDataset[keyword_upper]}
                objects['Aesculap'].display(temp)
            elif keyword_upper in IntegraDataset:
                description = IntegraDataset[keyword_upper]
                print(f"{keyword_upper}  {description}")
            elif keyword in MartinCatalog:
                print("Look up the KLS Catalog.")
            elif keyword in IntegraCatalog:
                print("Look up the INTEGRA catalog.")
            elif keyword in AesculapCatalog:
                print("Look up the AESCULAP catalog.")
            else:
                print("No match found for keyword.")
                if input("Re-enter keyword or 0 to terminate: ") == '0':
                    sys.exit(0)
        else:
            keys = keyword.split()
            if len(matching_products.keys()) > 300:
                confirm_input = input("More than 300 results. continue? (y) ")
                if confirm_input == 'y':
                    KLSUtils.display(matching_products, keys)
            else:
                KLSUtils.display(matching_products, keys)

    keyword_handlers = {
        'help': handle_help,
        'end': handle_terminate,
        'refresh': handle_refresh,
        'clear': handle_clear,
        'cls': handle_clear,
    }

    while True:
        command = input("Enter any key to start, 0 to terminate, 'help' to open guide: ").strip()

        if command == 'help':
            handle_help()
        elif command == '0':
            handle_terminate()
        else:
            print(f"Report:\nNumber of items acquired: {len(MartinDataset)}\nProceeding. . .")

            while True:
                keyword = input(Color.wrap_text("Enter keyword: ", Color.RED))
                keyword = string_cleaner(keyword)

                if keyword in keyword_handlers:
                    keyword_handlers[keyword]()
                    continue

                if keyword.endswith('rf'):
                    handle_reference(keyword)
                elif keyword.endswith('check'):
                    handle_check(keyword)
                elif keyword.endswith('inch'):
                    handle_inch(keyword)
                elif keyword.endswith('replace'):
                    handle_replace(keyword)
                elif keyword.endswith('load'):
                    handle_load(keyword)
                elif keyword.endswith('sculap'):
                    handle_sculap(keyword)
                elif keyword.endswith('integra'):
                    handle_integra(keyword)
                elif regex.fullmatch(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword):
                    if handle_search_by_code(keyword):
                        continue
                else:
                    handle_search(keyword)


if __name__ == '__main__':
    print("Source file : ",MartinSourceFile)
    main()