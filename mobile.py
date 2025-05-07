from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Random words to search
search_terms = [
    "Data science", "SpaceX", "tennis", "neural networks", "hurricane updates",
    "indie music", "tea culture", "natural language processing", "dog breeds", "backpacking",
    "software engineering", "HBO shows", "tech innovations", "Premier League", "film festivals", "ancient civilizations",
    "smart gadgets", "TypeScript", "nutrition advice", "Seoul travel",
    "street photography", "Mars missions", "cryptocurrency", "yoga poses", "plant-based meals",
    "mental health", "small businesses", "personal finance", "marine biology", "ethical hacking",
    "automation", "string theory", "piano tutorials", "classic novels", "breathing exercises",
    "esports tournaments", "real estate investing", "home improvement", "local cuisines", "urban design",
    "modern art", "wildlife care", "bilingual education", "style inspiration", "reinforcement learning",
    "wearable tech", "global warming", "trail running", "eco-friendly living", "startup culture"
]



# Set up the browser
mobile_emulation = { "deviceName": "Pixel 2" }

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)


chrome_options.add_argument(r"--user-data-dir=C:/Users/Windows/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.bing.com/")



for i in range(90):
    term = random.choice(search_terms) + " " + str(random.randint(1, 1000)) 
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    
    # Wait a bit to avoid detection
    time.sleep(random.uniform(5, 10))

driver.quit()