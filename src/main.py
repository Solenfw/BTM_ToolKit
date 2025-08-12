import sys
import os
from pathlib import Path
import traceback

os.system("")

# Import custom module
from BTM_Quote_Tool import load_config, AesculapUtils, IntegraUtils, KLSUtils
from BTM_Quote_Tool.cui.click_dispatcher import cli

if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.abspath(os.path.dirname(__file__))

# Path to config.json (already correct)
config_path = os.path.join(base_dir, "config.json")

# Load JSON config
config = load_config(config_path)

def get_absolute_path(relative_path):
    """Convert relative paths from config.json into absolute paths."""
    return os.path.join(base_dir, os.path.normpath(relative_path))

MartinSourceFile = Path(get_absolute_path(config['csv_source']['kls_product_csv']))
AesculapSourceFile = Path(get_absolute_path(config['csv_source']['aesculap_product_csv']))
IntegraSourceFile = Path(get_absolute_path(config['csv_source']['integra_product_csv']))

MartinSourceText = Path(get_absolute_path(config['source_text']['kls_text']))
IntegraSourceText = Path(get_absolute_path(config['source_text']['integra_text']))
AesculapSourceText = Path(get_absolute_path(config['source_text']['aesculap_text']))


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

    cli(obj={
        'MartinDataset': MartinDataset,
        'AesculapDataset': AesculapDataset,
        'IntegraDataset': IntegraDataset,
        'MartinSourceFile': MartinSourceFile,
        'objects': objects,
        'MartinCatalog': MartinCatalog,
        'IntegraCatalog': IntegraCatalog,
        'AesculapCatalog': AesculapCatalog
    })


if __name__ == '__main__':
    print("Source file : ",MartinSourceFile)
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        input("Press any key to exit.")
        sys.exit(1)
