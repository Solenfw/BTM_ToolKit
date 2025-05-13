from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import random
import logging
import argparse
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bing_search_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Random words to search - expanded with more variety
search_terms = [
    "Data science", "SpaceX", "tennis", "neural networks", "hurricane updates",
    "indie music", "tea culture", "natural language processing", "dog breeds", "backpacking",
    "software engineering", "HBO shows", "tech innovations", "Premier League", "film festivals", 
    "ancient civilizations", "smart gadgets", "TypeScript", "nutrition advice", "Seoul travel",
    "street photography", "Mars missions", "cryptocurrency", "yoga poses", "plant-based meals",
    "mental health", "small businesses", "personal finance", "marine biology", "ethical hacking",
    "automation", "string theory", "piano tutorials", "classic novels", "breathing exercises",
    "esports tournaments", "real estate investing", "home improvement", "local cuisines", "urban design",
    "modern art", "wildlife care", "bilingual education", "style inspiration", "reinforcement learning",
    "wearable tech", "global warming", "trail running", "eco-friendly living", "startup culture",
    "cloud computing", "electric vehicles", "photography tips", "remote work", "gardening ideas",
    "world history", "coffee brewing", "quantum physics", "digital marketing", "sustainable fashion"
]

def setup_driver(user_data_dir=None, profile_dir=None, headless=False):
    """Configure and return the WebDriver with specified options"""
    mobile_emulation = {"deviceName": "Pixel 2"}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if user_data_dir and profile_dir:
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument(f"--profile-directory={profile_dir}")
    
    if headless:
        chrome_options.add_argument("--headless=new")
    
    # Add some randomization to appear more human-like
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Set a random user agent
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Linux; Android 11; Pixel 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        })
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise

def perform_searches(driver, num_searches=30, delay_min=5, delay_max=12):
    """Perform the specified number of searches with randomized behavior"""
    successful_searches = 0
    
    try:
        driver.get("https://www.bing.com/")
        logger.info("Navigated to Bing homepage")
        
        # First wait for page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        for i in range(num_searches):
            try:
                # Generate a more natural search query
                if random.random() < 0.3:
                    # Sometimes use multiple terms
                    term = f"{random.choice(search_terms)} {random.choice(search_terms)}".lower()
                elif random.random() < 0.7:
                    # Sometimes add a number
                    term = f"{random.choice(search_terms)} {random.randint(1, 1000)}".lower()
                else:
                    # Sometimes just use the term
                    term = random.choice(search_terms).lower()
                
                # Add question format sometimes
                if random.random() < 0.25:
                    question_starters = ["how to", "what is", "why does", "when was", "where can I find"]
                    term = f"{random.choice(question_starters)} {term}"
                
                logger.info(f"Search {i+1}/{num_searches}: '{term}'")
                
                # Find and clear the search box
                search_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "q"))
                )
                search_box.clear()
                
                # Type like a human with random pauses between characters
                for char in term:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.01, 0.15))  # Random typing speed
                
                # Sometimes click the search button instead of pressing Enter
                if random.random() < 0.3:
                    try:
                        search_button = driver.find_element(By.ID, "search_icon")
                        search_button.click()
                    except (NoSuchElementException, StaleElementReferenceException):
                        search_box.send_keys(Keys.RETURN)
                else:
                    search_box.send_keys(Keys.RETURN)
                
                # Wait for search results to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "b_results"))
                )
                
                # Sometimes click on a search result
                if random.random() < 0.2:
                    try:
                        results = driver.find_elements(By.CSS_SELECTOR, "#b_results .b_algo a")
                        if results:
                            random_result = random.choice(results)
                            logger.info("Clicking on a search result")
                            random_result.click()
                            
                            # Wait on page for a bit
                            time.sleep(random.uniform(3, 7))
                            
                            # Go back
                            driver.back()
                            
                            # Make sure we're back at search results
                            WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, "b_results"))
                            )
                    except Exception as e:
                        logger.warning(f"Failed to click on a result: {e}")
                
                # Sometimes scroll down the page
                if random.random() < 0.5:
                    scroll_amount = random.randint(300, 1000)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(1, 3))
                
                # Variable wait time between searches to appear more human-like
                delay = random.uniform(delay_min, delay_max)
                logger.info(f"Waiting {delay:.2f} seconds before next search")
                time.sleep(delay)
                
                successful_searches += 1
                
            except TimeoutException:
                logger.warning(f"Timeout on search {i+1}. Retrying...")
                driver.get("https://www.bing.com/")
                time.sleep(random.uniform(3, 5))
                
            except Exception as e:
                logger.error(f"Error during search {i+1}: {e}")
                driver.get("https://www.bing.com/")
                time.sleep(random.uniform(3, 5))
    
    except Exception as e:
        logger.error(f"Critical error in perform_searches: {e}")
    
    finally:
        return successful_searches

def main():
    parser = argparse.ArgumentParser(description="Automate Bing searches for rewards")
    parser.add_argument("--searches", type=int, default=30, help="Number of searches to perform")
    parser.add_argument("--min-delay", type=float, default=5, help="Minimum delay between searches (seconds)")
    parser.add_argument("--max-delay", type=float, default=12, help="Maximum delay between searches (seconds)")
    parser.add_argument("--user-data-dir", type=str, help="Chrome user data directory")
    parser.add_argument("--profile-dir", type=str, default="Default", help="Chrome profile directory")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    logger.info(f"Starting Bing search automation at {start_time}")
    logger.info(f"Configured to perform {args.searches} searches with delays between {args.min_delay}-{args.max_delay} seconds")
    
    try:
        driver = setup_driver(args.user_data_dir, args.profile_dir, args.headless)
        successful_searches = perform_searches(
            driver, 
            num_searches=args.searches, 
            delay_min=args.min_delay,
            delay_max=args.max_delay
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        logger.info(f"Completed {successful_searches} successful searches out of {args.searches} attempts")
        logger.info(f"Script finished at {end_time} (ran for {duration:.2f} minutes)")
        
    except Exception as e:
        logger.error(f"Main execution error: {e}")
    
    finally:
        try:
            driver.quit()
            logger.info("Browser closed successfully")
        except:
            pass

if __name__ == "__main__":
    main()