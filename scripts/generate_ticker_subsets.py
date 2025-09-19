#!/usr/bin/env python3
"""
Script to generate ticker subsets for screener instances
"""

import os
import random

def load_tickers(market):
    """Load tickers from the appropriate file"""
    filepath = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt"
    
    if not os.path.exists(filepath):
        print(f"Ticker file not found: {filepath}")
        return []
    
    with open(filepath, 'r') as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    return tickers

def generate_subsets(market, num_subsets=10, tickers_per_subset=40):
    """Generate subsets of tickers for different screener instances"""
    tickers = load_tickers(market)
    
    if not tickers:
        return
    
    print(f"Generating {num_subsets} subsets for {market.upper()} market with {len(tickers)} total tickers")
    
    # Create directory for subsets
    subsets_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/subsets"
    os.makedirs(subsets_dir, exist_ok=True)
    
    # Generate subsets
    for i in range(1, num_subsets + 1):
        # Randomly sample tickers for this subset
        if len(tickers) <= tickers_per_subset:
            subset = tickers.copy()
        else:
            subset = random.sample(tickers, tickers_per_subset)
        
        # Sort for consistency
        subset.sort()
        
        # Save subset
        subset_file = f"{subsets_dir}/subset_{i:02d}.txt"
        with open(subset_file, 'w') as f:
            for ticker in subset:
                f.write(f"{ticker}\n")
        
        print(f"  Generated subset {i}: {len(subset)} tickers")
    
    # Also create a few sector-specific subsets (if applicable for India)
    if market == "india":
        create_sector_subsets(market, tickers)

def create_sector_subsets(market, all_tickers):
    """Create sector-specific subsets for India market"""
    # For India, we can extract sectors from the original CSV
    import csv
    
    csv_file = f"/Users/chiragpatnaik/Pinescript/{market}.csv"
    if not os.path.exists(csv_file):
        return
    
    # Read the CSV to get sector information
    sector_tickers = {}
    
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        
        for row in reader:
            if len(row) >= 4:
                ticker = row[1]
                sector = row[3]
                
                if sector not in sector_tickers:
                    sector_tickers[sector] = []
                sector_tickers[sector].append(ticker)
    
    # Create sector-specific subsets
    sectors_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/sectors"
    os.makedirs(sectors_dir, exist_ok=True)
    
    for sector, tickers in sector_tickers.items():
        # Clean sector name for filename
        clean_sector = "".join(c for c in sector if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_sector = clean_sector.replace(" ", "_")
        
        sector_file = f"{sectors_dir}/{clean_sector}.txt"
        with open(sector_file, 'w') as f:
            for ticker in sorted(tickers):
                f.write(f"{ticker}\n")
        
        print(f"  Created sector subset: {sector} ({len(tickers)} tickers)")

def generate_pine_script_format(market):
    """Generate Pine Script formatted ticker lists"""
    subsets_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/subsets"
    
    if not os.path.exists(subsets_dir):
        print(f"Subsets directory not found: {subsets_dir}")
        return
    
    pine_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/pine_script"
    os.makedirs(pine_dir, exist_ok=True)
    
    # Process each subset
    for i in range(1, 11):
        subset_file = f"{subsets_dir}/subset_{i:02d}.txt"
        
        if not os.path.exists(subset_file):
            continue
        
        with open(subset_file, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
        
        # Generate Pine Script format
        pine_content = f"// {market.upper()} Market Tickers - Instance {i}\n"
        pine_content += f"// Total: {len(tickers)} tickers\n\n"
        
        for j, ticker in enumerate(tickers, 1):
            # Add exchange prefix for proper TradingView format
            if market == "india":
                formatted_ticker = f"NSE:{ticker}" if not ticker.startswith("NSE:") else ticker
            else:  # US market
                formatted_ticker = ticker  # US tickers typically don't need prefix
            
            pine_content += f"s{j:02d} = input.symbol(\"{formatted_ticker}\", group = 'Symbols', inline = \"s{j:02d}\")\n"
        
        # Save Pine Script format
        pine_file = f"{pine_dir}/tickers_instance_{i:02d}.pine"
        with open(pine_file, 'w') as f:
            f.write(pine_content)
        
        print(f"  Generated Pine Script format for instance {i}")

def main():
    """Main function to generate all ticker subsets"""
    print("Generating ticker subsets for screener development...")
    
    # Generate subsets for both markets
    for market in ["india", "us"]:
        print(f"\nProcessing {market.upper()} market:")
        generate_subsets(market)
        generate_pine_script_format(market)
    
    print("\nTicker subset generation complete!")
    print("\nDirectory structure:")
    print("tickers/")
    print("├── india/")
    print("│   ├── all_tickers.txt")
    print("│   ├── subsets/")
    print("│   ├── sectors/")
    print("│   └── pine_script/")
    print("└── us/")
    print("    ├── all_tickers.txt")
    print("    ├── subsets/")
    print("    └── pine_script/")

if __name__ == "__main__":
    main()