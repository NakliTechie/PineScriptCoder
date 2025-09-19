import requests
from bs4 import BeautifulSoup
import json
import time
import os

def scrape_pine_script_reference(version="v6"):
    """
    Scrape Pine Script reference documentation and organize it by categories
    """
    url = f"https://www.tradingview.com/pine-script-reference/{version}/"
    
    # Create directory structure
    base_dir = f"pine_script_references/{version}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Send request to get the page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the main content structure
        # Look for the table of contents or main content area
        content = soup.find('main') or soup.find('div', class_='tv-content')
        
        if content:
            # Save the main content
            with open(f"{base_dir}/full_reference.html", "w", encoding="utf-8") as f:
                f.write(str(content))
            
            print(f"Saved full reference to {base_dir}/full_reference.html")
            
            # Try to extract categories and functions
            categories = extract_categories(soup, base_dir)
            
            # Save categories structure
            with open(f"{base_dir}/categories.json", "w", encoding="utf-8") as f:
                json.dump(categories, f, indent=2, ensure_ascii=False)
            
            print(f"Saved categories structure to {base_dir}/categories.json")
            
            return categories
        else:
            print("Could not find main content area")
            return None
            
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def extract_categories(soup, base_dir):
    """
    Extract categories and functions from the soup
    """
    categories = {}
    
    # Look for common patterns in documentation structure
    # Try to find accordion sections, table of contents, etc.
    toc_items = soup.find_all(['div', 'li', 'a'], class_=lambda x: x and ('toc' in x or 'accordion' in x or 'reference' in x))
    
    if toc_items:
        for i, item in enumerate(toc_items[:20]):  # Limit to first 20 for now
            text = item.get_text(strip=True)
            if text and len(text) > 2:
                categories[f"section_{i}"] = {
                    "title": text,
                    "class": item.get('class', []),
                    "id": item.get('id', ''),
                }
    else:
        # Fallback: look for any headers
        headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for i, header in enumerate(headers[:10]):
            text = header.get_text(strip=True)
            if text:
                categories[f"header_{i}"] = {
                    "title": text,
                    "tag": header.name,
                }
    
    return categories

def organize_by_version():
    """
    Organize references by version
    """
    versions = ["v3", "v4", "v5", "v6"]
    all_versions = {}
    
    for version in versions:
        print(f"Scraping Pine Script {version}...")
        categories = scrape_pine_script_reference(version)
        if categories:
            all_versions[version] = categories
        time.sleep(1)  # Be respectful to the server
    
    # Save overall structure
    with open("pine_script_references/versions.json", "w", encoding="utf-8") as f:
        json.dump(all_versions, f, indent=2, ensure_ascii=False)
    
    print("Saved version structure to pine_script_references/versions.json")

if __name__ == "__main__":
    organize_by_version()