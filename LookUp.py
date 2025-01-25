import regex
import csv
import sys
import os
from pathlib import Path

os.system("")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import custom modules
from BTM_Quote_Tool.string_utilities import string_cleaner
from BTM_Quote_Tool.config import load_config
from BTM_Quote_Tool.process import KLSUtils, AesculapUtils, IntegraUtils, Color, SupportUtils

# loading up data
config = load_config()
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
    while True:
        command = input("Enter any key to start, 0 to terminate, 'help' to open guide: ").strip()

        if command == 'help':
            SupportUtils.help()

        elif command == '0':
            print("Terminating. . . ")
            sys.exit(0)

        else:
            print(f"Report:\nNumber of items acquired: {len(MartinDataset)}\nProceeding. . .")

            while True:
                keyword = input(Color.wrap_text("Enter keyword: ", Color.RED))
                keyword = string_cleaner(keyword)
                
                if keyword == 'help':
                    SupportUtils.help()
                    continue

                if keyword == 'end':
                    print("Terminating. . . ")
                    sys.exit(0)

                if keyword.endswith('rf'):
                    SupportUtils.reference(keyword)
                    continue

                if keyword.endswith('check'):
                    SupportUtils.check(MartinDataset, keyword)
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
                        SupportUtils.replace(old_code, new_code)
                        continue
                    except Exception as err:
                        print(f"ERROR : {err}")
                        continue

                if keyword.endswith('load'):
                    keyword = keyword.replace('load', '').strip()
                    SupportUtils.save(keyword)
                    print("Product's code has been loaded.")
                    continue

                if keyword.endswith('sculap'):
                    keyword = keyword.replace('sculap', '').strip()
                    temp = objects['Aesculap'].search(keyword, AesculapDataset)
                    if temp:
                        objects['Aesculap'].display(temp)
                    continue

                if keyword.endswith('integra'):
                    product = keyword.replace('integra', '').strip()
                    objects['Integra'].search(product, IntegraDataset)
                    continue

                if keyword == 'refresh':
                    MartinDataset = objects['Martin'].DataProcess(MartinSourceFile)
                    print("Data has been updated. Continuing . . ")
                    continue

                if keyword.endswith('clear') or keyword.endswith('cls'):
                    os.system('cls')
                    continue

                if regex.fullmatch(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword):
                    if objects['Martin'].SearchByCode(keyword, AesculapDataset):
                        continue

                matching_products = objects['Martin'].search(keyword)

                if not matching_products:
                    keyword_upper = keyword.upper().strip()
                    
                    # keyword is an item of Aesculap 
                    if keyword_upper in AesculapDataset.keys():
                        temp = {keyword_upper: AesculapDataset[keyword_upper]}
                        objects['Aesculap'].display(temp)
                    
                    # keyword is an item of Integra
                    elif keyword_upper in IntegraDataset:
                        description = IntegraDataset[keyword_upper]
                        print(f"{keyword_upper}  {description}")

                    # Search for keyword among the .txt resources from Catalogs.
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


if __name__ == '__main__':
    print("Source file : ",MartinSourceFile)
    main()