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

def scrape_pine_script_reference_with_selenium(version="v6"):
    """Scrape Pine Script reference using Selenium to handle JavaScript-rendered content"""
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
        
        # Try to find the main content
        try:
            # Wait for the table of contents to load
            toc_element = driver.find_element(By.CLASS_NAME, "tv-script-reference__accordion")
            
            # Get the table of contents HTML
            toc_html = toc_element.get_attribute("outerHTML")
            
            # Save table of contents
            with open(f"{base_dir}/table_of_contents.html", "w", encoding="utf-8") as f:
                f.write(toc_html)
            
            print(f"Saved table of contents to {base_dir}/table_of_contents.html")
            
            # Extract categories from table of contents
            categories = extract_toc_categories(driver, toc_element)
            
            # Save categories structure
            with open(f"{base_dir}/categories_detailed.json", "w", encoding="utf-8") as f:
                json.dump(categories, f, indent=2, ensure_ascii=False)
            
            print(f"Saved detailed categories to {base_dir}/categories_detailed.json")
            
            # Get the main content
            try:
                content_element = driver.find_element(By.CLASS_NAME, "tv-script-reference__content-container")
                content_html = content_element.get_attribute("outerHTML")
                
                # Save main content
                with open(f"{base_dir}/main_content.html", "w", encoding="utf-8") as f:
                    f.write(content_html)
                
                print(f"Saved main content to {base_dir}/main_content.html")
            except Exception as e:
                print(f"Could not extract main content: {e}")
            
            return categories
            
        except Exception as e:
            print(f"Could not find table of contents: {e}")
            
            # Try to get any reference content
            try:
                reference_elements = driver.find_elements(By.CLASS_NAME, "tv-pine-reference")
                if reference_elements:
                    with open(f"{base_dir}/reference_elements.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"Saved full page source to {base_dir}/reference_elements.html")
                else:
                    # Save whatever content we can get
                    with open(f"{base_dir}/page_source.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"Saved page source to {base_dir}/page_source.html")
            except Exception as e2:
                print(f"Error saving page source: {e2}")
            
            return None
            
    except Exception as e:
        print(f"Error loading {url}: {str(e)}")
        return None
    finally:
        driver.quit()

def extract_toc_categories(driver, toc_element):
    """Extract categories and functions from the table of contents"""
    categories = {}
    
    try:
        # Find all accordion sections (categories)
        sections = toc_element.find_elements(By.CLASS_NAME, "tv-accordion__section")
        
        for i, section in enumerate(sections):
            try:
                # Get section header
                header = section.find_element(By.CLASS_NAME, "tv-accordion__trigger")
                header_text = header.text.strip()
                
                # Get section content (functions)
                content = section.find_element(By.CLASS_NAME, "tv-accordion__content")
                functions = content.find_elements(By.CLASS_NAME, "tv-pine-reference-toc-item")
                
                function_list = []
                for func in functions:
                    func_text = func.text.strip()
                    func_link = func.get_attribute("href") if func.tag_name == "a" else ""
                    function_list.append({
                        "name": func_text,
                        "link": func_link
                    })
                
                categories[f"category_{i}"] = {
                    "name": header_text,
                    "functions": function_list
                }
            except Exception as e:
                print(f"Error processing section {i}: {e}")
                continue
                
    except Exception as e:
        print(f"Error extracting TOC categories: {e}")
        
        # Fallback: try to get any headers
        try:
            headers = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
            for i, header in enumerate(headers[:10]):
                text = header.text.strip()
                if text:
                    categories[f"header_{i}"] = {
                        "title": text,
                        "tag": header.tag_name,
                    }
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
    
    return categories

def organize_references_with_selenium():
    """Organize all Pine Script references using Selenium"""
    versions = ["v6"]  # Start with v6, can add others later
    all_versions = {}
    
    for version in versions:
        print(f"Scraping Pine Script {version} with Selenium...")
        categories = scrape_pine_script_reference_with_selenium(version)
        if categories:
            all_versions[version] = categories
        time.sleep(2)  # Be respectful to the server
    
    # Save overall structure
    with open("pine_script_references/versions_detailed.json", "w", encoding="utf-8") as f:
        json.dump(all_versions, f, indent=2, ensure_ascii=False)
    
    print("Saved detailed version structure to pine_script_references/versions_detailed.json")

if __name__ == "__main__":
    organize_references_with_selenium()