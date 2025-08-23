import os
import sys
import regex
from ..process import SupportUtils, AesculapUtils, IntegraUtils, KLSUtils

class CommandHandler:
    def __init__(self, MartinDataset, AesculapDataset, IntegraDataset, MartinSourceFile, objects, MartinCatalog, IntegraCatalog, AesculapCatalog):
        self.MartinDataset = MartinDataset
        self.AesculapDataset = AesculapDataset
        self.IntegraDataset = IntegraDataset
        self.MartinSourceFile = MartinSourceFile
        self.objects = objects
        self.loop_data = [[]]
        self.MartinCatalog = MartinCatalog
        self.IntegraCatalog = IntegraCatalog
        self.AesculapCatalog = AesculapCatalog

    def handle_help(self, *args):
        SupportUtils.help()

    def handle_terminate(self, *args):
        print("Terminating. . . ")
        sys.exit(0)

    def handle_reference(self, *args):
        SupportUtils.reference(flags=args)

    def handle_check(self, *args):
        SupportUtils.check(self.MartinDataset, flags=args)

    def handle_inch(self, keyword):
        value_in_cm = int(regex.match(r'\d+', keyword).group())
        print(value_in_cm * 2.54)

    def handle_replace(self, keyword):
        try:
            match = regex.findall(r'\d{2}-\d{3}-\d{2}-\d{2}', keyword)
            old_code = match[0]
            new_code = match[1]
            SupportUtils.replace(old_code, new_code)
        except Exception as err:
            print(f"ERROR : {err}")

    def handle_load(self, keyword):
        keyword = keyword.replace('load', '').strip()
        SupportUtils.load(keyword)
        print("Product's code has been loaded.")
    
    def handle_pick(self, keyword):
        keyword = keyword.replace('get', '').strip()
        SupportUtils.pick(keyword, self.loop_data)
        print("Product's code has been picked.")

    def handle_sculap(self, keyword):
        keyword = keyword.replace('sculap', '').strip()
        temp = self.objects['Aesculap'].search(keyword, self.AesculapDataset)
        if temp:
            self.objects['Aesculap'].display(temp)

    def handle_integra(self, keyword):
        product = keyword.replace('integra', '').strip()
        self.objects['Integra'].search(product, self.IntegraDataset)

    def handle_refresh(self, *args):
        self.MartinDataset = self.objects['Martin'].DataProcess(self.MartinSourceFile)
        print("Data has been updated. Continuing . . ")

    def handle_clear(self, *args):
        os.system('cls' if os.name == 'nt' else 'clear')

    def handle_search_by_code(self, keyword):
        return self.objects['Martin'].SearchByCode(keyword, self.AesculapDataset)

    def handle_search(self, keyword):
        matching_products = self.objects['Martin'].search(keyword)
        if not matching_products:
            keyword_upper = keyword.upper().strip()
            if keyword_upper in self.AesculapDataset.keys():
                temp = {keyword_upper: self.AesculapDataset[keyword_upper]}
                self.objects['Aesculap'].display(temp)
            elif keyword_upper in self.IntegraDataset:
                description = self.IntegraDataset[keyword_upper]
                print(f"{keyword_upper}  {description}")
            elif keyword in self.MartinCatalog:
                print("Look up the KLS Catalog.")
            elif keyword in self.IntegraCatalog:
                print("Look up the INTEGRA catalog.")
            elif keyword in self.AesculapCatalog:
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
                temp = KLSUtils.display(matching_products, keys)
                self.loop_data = temp
