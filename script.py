from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


search_terms = [
    "Python", "NASA", "football", "machine learning", "weather",
    "music", "coffee", "artificial intelligence", "cat", "travel",
    "coding", "Netflix", "AI news", "NBA", "movies", "history",
    "technology", "JavaScript", "health tips", "Tokyo",
    "photography", "space exploration", "blockchain", "fitness routines", "vegan recipes",
    "mindfulness", "startups", "economics", "ocean life", "cybersecurity",
    "robotics", "quantum computing", "guitar lessons", "book recommendations", "meditation",
    "gaming news", "stock market", "DIY crafts", "street food", "architecture",
    "art trends", "pet care", "language learning", "fashion tips", "deep learning",
    "mobile apps", "climate change", "mountain hiking", "sustainability", "entrepreneurship"
]



driver = webdriver.Edge()

driver.get("https://www.bing.com/")


for i in range(90):
    term = random.choice(search_terms) + " " + str(random.randint(1, 1000)) 
    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    
    # Wait a bit to avoid detection
    time.sleep(random.uniform(7, 10))

driver.quit()
