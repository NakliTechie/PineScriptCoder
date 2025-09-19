import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Set up Chrome driver with options for headless browsing"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_all_versions_toc():
    """Scrape table of contents for all Pine Script versions"""
    versions = ["v3", "v4", "v5", "v6"]
    
    for version in versions:
        url = f"https://www.tradingview.com/pine-script-reference/{version}/"
        
        # Create directory structure
        base_dir = f"pine_script_references/{version}"
        os.makedirs(base_dir, exist_ok=True)
        
        # Set up driver
        driver = setup_driver()
        
        try:
            print(f"Loading {url}...")
            driver.get(url)
            
            # Wait for content to load
            time.sleep(5)
            
            # Try to find the table of contents
            try:
                toc_element = driver.find_element(By.CLASS_NAME, "tv-script-reference__accordion")
                
                # Get the table of contents HTML
                toc_html = toc_element.get_attribute("outerHTML")
                
                # Save table of contents
                with open(f"{base_dir}/table_of_contents.html", "w", encoding="utf-8") as f:
                    f.write(toc_html)
                
                print(f"Saved table of contents for {version} to {base_dir}/table_of_contents.html")
                
            except Exception as e:
                print(f"Could not find table of contents for {version}: {e}")
                
        except Exception as e:
            print(f"Error loading {url}: {str(e)}")
        finally:
            driver.quit()
        
        time.sleep(2)  # Be respectful to the server

if __name__ == "__main__":
    scrape_all_versions_toc()