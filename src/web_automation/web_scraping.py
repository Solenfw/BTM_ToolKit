'''
For Aesculap Website catalog specifically.
'''

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from BTM_Quote_Tool.config import load_config

config = load_config()
input_code_file = Path(config['tests']['input_file']).resolve()


# Color class for console output
os.system("")
class Color:
    CYAN = '\033[1;96m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    RED = '\033[1;31m'
    END = '\033[0m'
    
    @staticmethod
    def wrap_text(text, color):
        return f"{color}{text}{Color.END}"

# Function to read product codes from a file
def read_product_codes(file_path):
    with open(file_path, 'r') as file:
        codes = file.read().splitlines()
    return codes

# Initialize Selenium options for headless mode
options = Options()
options.headless = True
service = FirefoxService()  
driver = webdriver.Firefox(service=service, options=options)

# Store descriptions as a list of dictionaries
descriptions = []
counter = 1

try:
    driver.get("https://surgical-instruments.bbraun.com/en-01")

    try:
        # Click the 'Allow Cookies' button if it exists
        allow_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Allow Cookies']/parent::button"))
        )
        allow_cookies_button.click()
        print("Successfully clicked 'Allow Cookies' button.")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Read product codes from the file
    product_codes = read_product_codes(input_code_file)
    time.sleep(3)

    # Loop through each product code
    for code in product_codes:
        counter += 1
        if counter == 1000:
            break
        search_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='searchComponentInput']")
        search_input.clear()  
        search_input.send_keys(code)  
        search_input.send_keys(Keys.RETURN)  # Press Enter

        try:
            # Check for absence message
            absence_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'The item number you were looking for is not available.')]"))
            )
            print(f"No description found for {Color.CYAN}{code}{Color.END}.")
            descriptions.append({"code": code, "description": "none"})  # Append 'none' if no description is found
        except:
            # Retrieve product description if absence message is not found
            try:
                description_element = driver.find_element(By.CSS_SELECTOR, "h2.RenderHTML[data-testid='render-html']")
                product_description = description_element.text
                print(f"Found description for {Color.CYAN}{code}{Color.END}.")
                descriptions.append({"code": code, "description": product_description})  # Append description to list
            except Exception as e:
                print(f"No description found for {Color.CYAN}{code}{Color.END}.")
                descriptions.append({"code": code, "description": "none"})  # Append 'none' in case of failure

finally:
    driver.quit()  # Close the browser

# Write all descriptions to a CSV file at once
with open('descriptions.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['code', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(descriptions)

print("All descriptions have been written to descriptions.csv.")
