# Utility Scripts

This directory contains Python scripts for managing and organizing the Pine Script development framework.

## Script Descriptions

### Checkpoint Management
- `checkpoint_manager.py` - Main checkpoint management system
- `simple_checkpoint.py` - Simplified checkpoint utility
- `checkpoint_example.py` - Example usage of checkpoint system

### Reference Management
- `scrape_pine_reference.py` - Scrape Pine Script reference from TradingView
- `scrape_pine_reference_selenium.py` - Alternative scraping using Selenium
- `scrape_all_versions.py` - Scrape all Pine Script versions
- `parse_toc.py` - Parse table of contents from reference pages
- `parse_all_versions.py` - Parse all scraped versions
- `organize_pine_reference.py` - Organize scraped references into categories
- `convert_to_pdf.py` - Convert markdown references to PDF
- `pineref2pdf.py` - Alternative PDF conversion tool

## Usage Examples

### Scraping Pine Script References
```bash
# Scrape a specific version
python scripts/scrape_pine_reference.py v6

# Scrape all versions
python scripts/scrape_all_versions.py

# Organize scraped references
python scripts/organize_pine_reference.py
```

### Checkpoint Management
```bash
# Create a new checkpoint
python scripts/checkpoint_manager.py create "Project Name" "Task Description"

# List existing checkpoints
python scripts/checkpoint_manager.py list

# Resume from latest checkpoint
python scripts/checkpoint_manager.py resume
```

## Requirements

Most scripts require:
- Python 3.6+
- requests library
- beautifulsoup4 library
- selenium (for selenium-based scraping)

Install requirements:
```bash
pip install requests beautifulsoup4 selenium
```