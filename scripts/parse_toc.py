import re
import json
import os
from bs4 import BeautifulSoup

def parse_pine_script_toc():
    """Parse the Pine Script table of contents and create a proper organization"""
    
    # Read the table of contents file
    toc_file = "pine_script_references/v6/table_of_contents.html"
    
    if not os.path.exists(toc_file):
        print(f"File {toc_file} not found")
        return
    
    with open(toc_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all section headers and their content
    organized_content = {
        "categories": {},
        "all_items": []
    }
    
    # Find all section headers (categories)
    headers = soup.find_all(class_="tv-accordion__section-header")
    
    for header in headers:
        # Get category name
        category_name = header.get_text(strip=True)
        
        # Find the next sibling which should be the section body
        section_body = header.find_next_sibling(class_="tv-accordion__section-body")
        
        if section_body:
            # Find all items in this section
            items = section_body.find_all(class_="tv-pine-reference-toc-item")
            
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
            print(f"Found {len(category_items)} items in category '{category_name}'")
    
    # Save the organized structure
    with open("pine_script_references/v6/organized_content.json", "w", encoding="utf-8") as f:
        json.dump(organized_content, f, indent=2, ensure_ascii=False)
    
    print(f"Total categories: {len(organized_content['categories'])}")
    print(f"Total items: {len(organized_content['all_items'])}")
    
    # Create markdown organization
    create_markdown_organization(organized_content)
    
    return organized_content

def determine_item_type(name):
    """Determine the type of item based on its name"""
    if '(' in name and ')' in name:
        return "function"
    elif name.startswith("var_"):
        return "variable"
    elif '.' in name:
        return "property"
    elif name.isupper() and len(name) < 20:
        return "constant"
    else:
        return "variable"

def create_markdown_organization(organized_content):
    """Create a markdown organization of the content"""
    base_dir = "pine_script_references/v6"
    
    # Create categories directory
    categories_dir = os.path.join(base_dir, "categories")
    os.makedirs(categories_dir, exist_ok=True)
    
    # Create markdown files for each category
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
                markdown_content += f"- `{func['name']}`\n"
            markdown_content += "\n"
        
        if variables:
            markdown_content += "## Variables\n\n"
            for var in variables:
                markdown_content += f"- `{var['name']}`\n"
            markdown_content += "\n"
        
        if properties:
            markdown_content += "## Properties\n\n"
            for prop in properties:
                markdown_content += f"- `{prop['name']}`\n"
            markdown_content += "\n"
        
        if constants:
            markdown_content += "## Constants\n\n"
            for const in constants:
                markdown_content += f"- `{const['name']}`\n"
            markdown_content += "\n"
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
    
    print(f"Created {len(organized_content['categories'])} markdown files in {categories_dir}")
    
    # Create main README
    create_main_readme(organized_content, base_dir)

def create_main_readme(organized_content, base_dir):
    """Create a main README file"""
    readme_path = os.path.join(base_dir, "README.md")
    
    content = "# Pine Script v6 Reference Manual\n\n"
    content += "This is an organized reference for Pine Script v6 functions, variables, and constants.\n\n"
    
    # Table of contents
    content += "## Categories\n\n"
    
    for category_name, items in organized_content["categories"].items():
        # Create a safe filename for linking
        safe_filename = re.sub(r'[^\w\s-]', '', category_name).strip().lower()
        safe_filename = re.sub(r'[-\s]+', '_', safe_filename) + ".md"
        
        content += f"- [{category_name}](categories/{safe_filename})\n"
        
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
    for item_type, count in sorted(type_counts.items()):
        content += f"- **{item_type.capitalize()}s:** {count}\n"
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Created main README at {readme_path}")

if __name__ == "__main__":
    parse_pine_script_toc()