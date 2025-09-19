import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

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

def scrape_and_organize_pine_script_reference(version="v6"):
    """Scrape Pine Script reference and organize it into a proper structure"""
    url = f"https://www.tradingview.com/pine-script-reference/{version}/"
    
    # Create directory structure
    base_dir = f"pine_script_references/{version}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Create subdirectories for different types of content
    categories_dir = os.path.join(base_dir, "categories")
    functions_dir = os.path.join(base_dir, "functions")
    variables_dir = os.path.join(base_dir, "variables")
    
    for directory in [categories_dir, functions_dir, variables_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Set up driver
    driver = setup_driver()
    
    try:
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for content to load
        time.sleep(5)
        
        # Get the full page source after JavaScript execution
        page_source = driver.page_source
        
        # Save full page source
        with open(f"{base_dir}/full_page_source.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract table of contents
        toc_element = soup.find(class_="tv-script-reference__accordion")
        if toc_element:
            # Save table of contents
            with open(f"{base_dir}/table_of_contents.html", "w", encoding="utf-8") as f:
                f.write(str(toc_element))
            
            # Parse and organize the content
            organized_content = parse_table_of_contents(toc_element, soup, base_dir)
            
            # Save organized structure
            with open(f"{base_dir}/organized_structure.json", "w", encoding="utf-8") as f:
                json.dump(organized_content, f, indent=2, ensure_ascii=False)
            
            print(f"Saved organized structure to {base_dir}/organized_structure.json")
            
            # Create markdown files for each category
            create_markdown_files(organized_content, base_dir)
            
            return organized_content
        
        return None
            
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None
    finally:
        driver.quit()

def parse_table_of_contents(toc_element, soup, base_dir):
    """Parse the table of contents and organize content by categories"""
    organized_content = {
        "categories": {},
        "all_items": []
    }
    
    # Find all sections in the table of contents
    sections = toc_element.find_all(class_="tv-accordion__section")
    
    for section in sections:
        # Get section header
        header_elem = section.find(class_="tv-accordion__section-header")
        if not header_elem:
            continue
            
        category_name = header_elem.get_text(strip=True)
        print(f"Processing category: {category_name}")
        
        # Get all items in this section
        items = section.find_all(class_="tv-pine-reference-toc-item")
        
        category_items = []
        for item in items:
            item_name = item.get_text(strip=True)
            item_href = item.get('href', '').lstrip('#')
            item_data_name = item.get('data-name', '')
            
            # Determine item type based on name patterns
            item_type = determine_item_type(item_name)
            
            item_info = {
                "name": item_name,
                "href": item_href,
                "data_name": item_data_name,
                "type": item_type
            }
            
            category_items.append(item_info)
            organized_content["all_items"].append(item_info)
        
        organized_content["categories"][category_name] = category_items
    
    return organized_content

def determine_item_type(name):
    """Determine the type of item based on its name"""
    if '(' in name and ')' in name:
        return "function"
    elif '.' in name:
        return "property"
    elif name.isupper() and len(name) < 10:
        return "constant"
    else:
        return "variable"

def create_markdown_files(organized_content, base_dir):
    """Create markdown files for each category"""
    categories_dir = os.path.join(base_dir, "categories")
    
    for category_name, items in organized_content["categories"].items():
        # Create a safe filename
        safe_filename = re.sub(r'[^\w\s-]', '', category_name).strip().lower()
        safe_filename = re.sub(r'[-\s]+', '_', safe_filename) + ".md"
        
        filepath = os.path.join(categories_dir, safe_filename)
        
        # Create markdown content
        markdown_content = f"# {category_name}\n\n"
        
        # Group items by type
        functions = [item for item in items if item["type"] == "function"]
        variables = [item for item in items if item["type"] == "variable"]
        properties = [item for item in items if item["type"] == "property"]
        constants = [item for item in items if item["type"] == "constant"]
        
        if functions:
            markdown_content += "## Functions\n\n"
            for func in functions:
                markdown_content += f"- [{func['name']}](#{func['href']})\n"
            markdown_content += "\n"
        
        if variables:
            markdown_content += "## Variables\n\n"
            for var in variables:
                markdown_content += f"- [{var['name']}](#{var['href']})\n"
            markdown_content += "\n"
        
        if properties:
            markdown_content += "## Properties\n\n"
            for prop in properties:
                markdown_content += f"- [{prop['name']}](#{prop['href']})\n"
            markdown_content += "\n"
        
        if constants:
            markdown_content += "## Constants\n\n"
            for const in constants:
                markdown_content += f"- [{const['name']}](#{const['href']})\n"
            markdown_content += "\n"
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
    
    print(f"Created markdown files in {categories_dir}")

def create_main_readme(organized_content, base_dir):
    """Create a main README file with an overview of all content"""
    readme_path = os.path.join(base_dir, "README.md")
    
    content = "# Pine Script Reference Manual\n\n"
    content += "This is an organized reference for Pine Script functions, variables, and constants.\n\n"
    
    # Table of contents
    content += "## Table of Contents\n\n"
    
    for category_name, items in organized_content["categories"].items():
        # Create a safe anchor link
        anchor = re.sub(r'[^\w\s-]', '', category_name).strip().lower()
        anchor = re.sub(r'[-\s]+', '-', anchor)
        
        content += f"- [{category_name}](categories/#{anchor})\n"
        
        # Brief summary of items in category
        functions = len([item for item in items if item["type"] == "function"])
        variables = len([item for item in items if item["type"] == "variable"])
        properties = len([item for item in items if item["type"] == "property"])
        constants = len([item for item in items if item["type"] == "constant"])
        
        summary_parts = []
        if functions > 0:
            summary_parts.append(f"{functions} functions")
        if variables > 0:
            summary_parts.append(f"{variables} variables")
        if properties > 0:
            summary_parts.append(f"{properties} properties")
        if constants > 0:
            summary_parts.append(f"{constants} constants")
        
        if summary_parts:
            content += f"  - {', '.join(summary_parts)}\n"
    
    content += "\n## Total Items\n\n"
    total_items = len(organized_content["all_items"])
    content += f"- **Total items:** {total_items}\n\n"
    
    # Type breakdown
    type_counts = {}
    for item in organized_content["all_items"]:
        item_type = item["type"]
        type_counts[item_type] = type_counts.get(item_type, 0) + 1
    
    content += "### By Type\n\n"
    for item_type, count in type_counts.items():
        content += f"- **{item_type.capitalize()}s:** {count}\n"
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Created main README at {readme_path}")

def organize_all_versions():
    """Organize all Pine Script versions"""
    versions = ["v6"]  # Start with v6
    all_versions_summary = {}
    
    for version in versions:
        print(f"Processing Pine Script {version}...")
        organized_content = scrape_and_organize_pine_script_reference(version)
        
        if organized_content:
            all_versions_summary[version] = {
                "categories": list(organized_content["categories"].keys()),
                "total_items": len(organized_content["all_items"])
            }
            
            # Create main README for this version
            base_dir = f"pine_script_references/{version}"
            create_main_readme(organized_content, base_dir)
    
    # Create overall summary
    with open("pine_script_references/SUMMARY.md", "w", encoding="utf-8") as f:
        f.write("# Pine Script References Summary\n\n")
        for version, info in all_versions_summary.items():
            f.write(f"## {version}\n\n")
            f.write(f"- **Total items:** {info['total_items']}\n")
            f.write(f"- **Categories:** {', '.join(info['categories'])}\n\n")
    
    print("Created overall summary at pine_script_references/SUMMARY.md")

if __name__ == "__main__":
    organize_all_versions()