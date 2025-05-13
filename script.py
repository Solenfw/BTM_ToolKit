from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        logging.FileHandler("bing_edge_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Random words to search - enhanced list with more variety
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
    "mobile apps", "climate change", "mountain hiking", "sustainability", "entrepreneurship",
    "web development", "remote work", "online courses", "digital nomads", "science news",
    "solar energy", "virtual reality", "3D printing", "classic cars", "podcasts",
    "home automation", "gardening tips", "cooking techniques", "board games", "astronomy"
]

def setup_driver(headless=False):
    """Configure and return the Edge WebDriver with specified options"""
    options = webdriver.EdgeOptions()
    
    if headless:
        options.add_argument("--headless=new")
    
    # Add some randomization to appear more human-like
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Edge(options=options)
        # Set a random user agent
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        })
        return driver
    except Exception as e:
        logger.error(f"Failed to initialize Edge WebDriver: {e}")
        raise

def generate_search_term():
    """Generate a natural-looking search query"""
    rand = random.random()
    
    if rand < 0.25:
        # Basic search with number
        term = f"{random.choice(search_terms)} {random.randint(1, 1000)}"
    elif rand < 0.5:
        # Just the search term
        term = random.choice(search_terms)
    elif rand < 0.75:
        # Combination of two terms
        term = f"{random.choice(search_terms)} and {random.choice(search_terms)}"
    else:
        # Question format
        question_starters = ["how to", "what is", "why does", "when was", "where can I find", "is there"]
        term = f"{random.choice(question_starters)} {random.choice(search_terms).lower()}"
        
    return term.lower()

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
                # Generate search term
                term = generate_search_term()
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
                if random.random() < 0.25:
                    try:
                        results = driver.find_elements(By.CSS_SELECTOR, "#b_results .b_algo a")
                        if results:
                            result_index = min(random.randint(0, 5), len(results) - 1)  # Focus on top results
                            random_result = results[result_index]
                            logger.info(f"Clicking on search result #{result_index+1}")
                            random_result.click()
                            
                            # Wait on page for a bit
                            time.sleep(random.uniform(4, 8))
                            
                            # Sometimes scroll on the resulting page
                            if random.random() < 0.6:
                                scroll_amount = random.randint(300, 1200)
                                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                                time.sleep(random.uniform(2, 4))
                                
                                # Sometimes scroll back up
                                if random.random() < 0.5:
                                    driver.execute_script(f"window.scrollBy(0, -{scroll_amount//2});")
                                    time.sleep(random.uniform(1, 2))
                            
                            # Go back
                            driver.back()
                            
                            # Make sure we're back at search results
                            WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, "b_results"))
                            )
                    except Exception as e:
                        logger.warning(f"Failed to interact with a result: {e}")
                
                # Sometimes scroll down the search results
                elif random.random() < 0.6:
                    scroll_amount = random.randint(300, 800)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(1, 3))
                    
                    # Sometimes scroll back up
                    if random.random() < 0.4:
                        driver.execute_script(f"window.scrollBy(0, -{scroll_amount//2});")
                        time.sleep(random.uniform(1, 2))
                
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
    parser = argparse.ArgumentParser(description="Automate Bing searches with Microsoft Edge")
    parser.add_argument("--searches", type=int, default=90, help="Number of searches to perform")
    parser.add_argument("--min-delay", type=float, default=7, help="Minimum delay between searches (seconds)")
    parser.add_argument("--max-delay", type=float, default=10, help="Maximum delay between searches (seconds)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    logger.info(f"Starting Bing search automation with Edge at {start_time}")
    logger.info(f"Configured to perform {args.searches} searches with delays between {args.min_delay}-{args.max_delay} seconds")
    
    try:
        driver = setup_driver(args.headless)
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