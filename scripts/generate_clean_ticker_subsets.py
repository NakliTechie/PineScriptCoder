#!/usr/bin/env python3
"""
Script to generate clean ticker subsets for screener instances
"""

import os
import random
import csv

def load_tickers(market):
    """Load tickers from the appropriate file"""
    filepath = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt"
    
    if not os.path.exists(filepath):
        print(f"Ticker file not found: {filepath}")
        return []
    
    with open(filepath, 'r') as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    # Remove duplicates and sort
    tickers = sorted(list(set(tickers)))
    return tickers

def create_sector_subsets(market):
    """Create clean sector-specific subsets for India market"""
    csv_file = f"/Users/chiragpatnaik/Pinescript/{market}.csv"
    if not os.path.exists(csv_file):
        return {}
    
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
                    sector_tickers[sector] = set()
                sector_tickers[sector].add(ticker)
    
    # Create sector-specific subsets
    sectors_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/sectors"
    os.makedirs(sectors_dir, exist_ok=True)
    
    sector_files = {}
    for sector, tickers in sector_tickers.items():
        # Clean sector name for filename
        clean_sector = "".join(c for c in sector if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_sector = clean_sector.replace(" ", "_").replace("&", "and")
        
        sector_file = f"{sectors_dir}/{clean_sector}.txt"
        with open(sector_file, 'w') as f:
            for ticker in sorted(tickers):
                f.write(f"{ticker}\n")
        
        sector_files[sector] = len(tickers)
        print(f"  Created sector subset: {sector} ({len(tickers)} unique tickers)")
    
    return sector_files

def generate_subsets(market, num_subsets=10, tickers_per_subset=40):
    """Generate subsets of tickers for different screener instances"""
    tickers = load_tickers(market)
    
    if not tickers:
        return
    
    print(f"Generating {num_subsets} subsets for {market.upper()} market with {len(tickers)} total unique tickers")
    
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
    
    # For India market, also create sector-specific subsets
    if market == "india":
        sector_files = create_sector_subsets(market)

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

def create_popular_subsets(market):
    """Create subsets of popular/most-traded tickers"""
    if market == "india":
        # For India, we can use some common large-cap stocks
        popular_tickers = [
            "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK",
            "SBIN", "BHARTIARTL", "ITC", "LT", "AXISBANK", "ASIANPAINT",
            "MARUTI", "SUNPHARMA", "TATAMOTORS", "TITAN", "WIPRO", "ULTRACEMCO",
            "M&M", "NESTLEIND", "TECHM", "BAJFINANCE", "ADANIPORTS", "ONGC"
        ]
    else:  # US
        # For US, common large-cap stocks
        popular_tickers = [
            "AAPL", "MSFT", "AMZN", "FB", "GOOGL", "GOOG", "TSLA", "BRK.B",
            "JPM", "JNJ", "V", "PG", "UNH", "MA", "DIS", "NVDA", "HD", "BAC",
            "PYPL", "CMCSA", "NFLX", "ADBE", "VZ", "T", "PFE", "XOM", "KO",
            "INTC", "CSCO", "WMT", "ABT", "CRM", "TMO", "PEP", "ABBV"
        ]
    
    # Save popular tickers subset
    popular_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular"
    os.makedirs(popular_dir, exist_ok=True)
    
    popular_file = f"{popular_dir}/popular_tickers.txt"
    with open(popular_file, 'w') as f:
        for ticker in sorted(popular_tickers):
            f.write(f"{ticker}\n")
    
    print(f"  Created popular tickers subset: {len(popular_tickers)} tickers")

def main():
    """Main function to generate all ticker subsets"""
    print("Generating clean ticker subsets for screener development...")
    
    # Generate subsets for both markets
    for market in ["india", "us"]:
        print(f"\nProcessing {market.upper()} market:")
        generate_subsets(market)
        generate_pine_script_format(market)
        create_popular_subsets(market)
    
    print("\nClean ticker subset generation complete!")
    print("\nDirectory structure:")
    print("tickers/")
    print("├── india/")
    print("│   ├── all_tickers.txt")
    print("│   ├── subsets/")
    print("│   ├── sectors/")
    print("│   ├── popular/")
    print("│   └── pine_script/")
    print("└── us/")
    print("    ├── all_tickers.txt")
    print("    ├── subsets/")
    print("    ├── popular/")
    print("    └── pine_script/")

if __name__ == "__main__":
    main()