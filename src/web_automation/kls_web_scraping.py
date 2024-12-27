from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

""" For KLS MARTIN web-based catalogue specifically. """

with open("product_codes.txt", "r") as file:
    codes = [line.strip() for line in file if line.strip()]

# Set up Selenium WebDriver
options = Options()
options.headless = True
service = webdriver.FirefoxService()  
driver = webdriver.Firefox(service=service, options=options)

url = "https://www.klsmartin.com/catalog/en/"  

driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 5)

# Storage for results
results = []

try:
    for index, code in enumerate(codes):
        try:
            if index == 1000:
                break
            # Locate the search input bar and enter the code
            search_bar = wait.until(EC.presence_of_element_located((By.NAME, "search-text")))
            search_bar.clear()  
            search_bar.send_keys(code)
            search_bar.send_keys(Keys.RETURN)  

            # Wait for the search results to load
            time.sleep(1) 

            # Check if there are results
            search_result_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.content-wrap")))
            if "(1)" in search_result_header.text:  
                # Extract item details
                description_element = driver.find_element(By.CSS_SELECTOR, ".td-2 .content")
                description = description_element.text.strip()
                results.append((code, description))
                print(f"Got one: {code} - {description}")
            else:
                results.append((code, "No result found"))
                print("No description found.")
        except Exception as e:
            print(f"Error processing code {code}: {e}")
            results.append((code, "Error"))
finally:
    # Close the browser
    driver.quit()

with open("product_descriptions.txt", "a", encoding='utf-8') as file:
    for code, description in results:
        file.write(f"{code}: {description}\n")

print("Scraping completed. Results saved to results.txt.")
