#!/usr/bin/env python3
"""
Script to convert Pine Script reference markdown files to PDF
"""

import os
import subprocess
import sys

def convert_md_to_pdf(markdown_file, pdf_file):
    """
    Convert a markdown file to PDF using pandoc or weasyprint
    """
    try:
        # Try using pandoc first (if available)
        subprocess.run([
            'pandoc', 
            markdown_file, 
            '-o', pdf_file,
            '--pdf-engine=xelatex',
            '--toc',
            '--toc-depth=2'
        ], check=True)
        print(f"Converted {markdown_file} to {pdf_file} using pandoc")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try using markdown-to-pdf (if available)
            subprocess.run([
                'markdown-pdf', 
                markdown_file, 
                '-o', pdf_file
            ], check=True)
            print(f"Converted {markdown_file} to {pdf_file} using markdown-pdf")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Could not convert {markdown_file} to PDF - no suitable tool found")
            return False

def convert_all_references_to_pdf():
    """
    Convert all Pine Script reference markdown files to PDF
    """
    base_dir = "pine_script_references"
    
    # Check if any PDF conversion tools are available
    tools = []
    try:
        subprocess.run(['pandoc', '--version'], check=True, stdout=subprocess.DEVNULL)
        tools.append('pandoc')
    except FileNotFoundError:
        pass
    
    try:
        subprocess.run(['markdown-pdf', '--help'], check=True, stdout=subprocess.DEVNULL)
        tools.append('markdown-pdf')
    except FileNotFoundError:
        pass
    
    if not tools:
        print("No PDF conversion tools found. Please install either:")
        print("  - pandoc (https://pandoc.org/)")
        print("  - markdown-pdf (npm install -g markdown-pdf)")
        return
    
    print(f"Found PDF conversion tools: {', '.join(tools)}")
    
    # Convert README files for each version
    versions = ["v3", "v4", "v5", "v6"]
    
    for version in versions:
        readme_path = os.path.join(base_dir, version, "README.md")
        pdf_path = os.path.join(base_dir, version, f"pine_script_{version}_reference.pdf")
        
        if os.path.exists(readme_path):
            convert_md_to_pdf(readme_path, pdf_path)
        else:
            print(f"README.md not found for {version}")
    
    # Convert category files for v6 as an example
    categories_dir = os.path.join(base_dir, "v6", "categories")
    if os.path.exists(categories_dir):
        pdf_categories_dir = os.path.join(base_dir, "v6", "pdf_categories")
        os.makedirs(pdf_categories_dir, exist_ok=True)
        
        for filename in os.listdir(categories_dir):
            if filename.endswith(".md"):
                md_path = os.path.join(categories_dir, filename)
                pdf_filename = filename.replace(".md", ".pdf")
                pdf_path = os.path.join(pdf_categories_dir, pdf_filename)
                convert_md_to_pdf(md_path, pdf_path)

def create_combined_reference():
    """
    Create a combined reference document
    """
    combined_content = "# Pine Script References - All Versions\n\n"
    
    versions = ["v3", "v4", "v5", "v6"]
    
    for version in versions:
        readme_path = os.path.join("pine_script_references", version, "README.md")
        if os.path.exists(readme_path):
            combined_content += f"\n\n---\n\n## Pine Script {version}\n\n"
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Remove the title since we're adding our own
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    content = '\n'.join(lines[1:])
                combined_content += content
    
    combined_file = "pine_script_references/combined_reference.md"
    with open(combined_file, "w", encoding="utf-8") as f:
        f.write(combined_content)
    
    print(f"Created combined reference at {combined_file}")
    
    # Try to convert to PDF
    pdf_file = "pine_script_references/combined_reference.pdf"
    convert_md_to_pdf(combined_file, pdf_file)

if __name__ == "__main__":
    print("Pine Script Reference PDF Converter")
    print("===================================")
    
    # Convert all references to PDF
    convert_all_references_to_pdf()
    
    # Create combined reference
    create_combined_reference()
    
    print("\nDone! Check the pine_script_references directory for PDF files.")