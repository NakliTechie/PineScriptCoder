#!/usr/bin/env python3
"""
Quick ticker access script for screener development
"""

import os
import random

def get_tickers(market, category="subsets", instance=1):
    """
    Get tickers for a specific market and category
    
    Args:
        market (str): "india" or "us"
        category (str): "subsets", "sectors", "popular", or "all"
        instance (int): Instance number (1-10) for subsets, sector name for sectors
    
    Returns:
        list: List of tickers
    """
    base_path = f"/Users/chiragpatnaik/Pinescript/tickers/{market}"
    
    if category == "subsets":
        file_path = f"{base_path}/subsets/subset_{instance:02d}.txt"
    elif category == "popular":
        file_path = f"{base_path}/popular/popular_tickers.txt"
    elif category == "all":
        file_path = f"{base_path}/all_tickers.txt"
    elif category == "sectors":
        # For sectors, instance should be the sector name
        file_path = f"{base_path}/sectors/{instance}.txt"
    else:
        print(f"Unknown category: {category}")
        return []
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r') as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    return tickers

def print_pine_script_format(market, category="subsets", instance=1):
    """
    Print tickers in Pine Script format
    """
    tickers = get_tickers(market, category, instance)
    
    if not tickers:
        return
    
    print(f"// {market.upper()} Market Tickers - {category} - {instance}")
    print(f"// Total: {len(tickers)} tickers\n")
    
    for i, ticker in enumerate(tickers, 1):
        # Add exchange prefix for proper TradingView format
        if market == "india":
            formatted_ticker = f"NSE:{ticker}" if not ticker.startswith("NSE:") else ticker
        else:  # US market
            formatted_ticker = ticker
        
        print(f"s{i:02d} = input.symbol(\"{formatted_ticker}\", group = 'Symbols', inline = \"s{i:02d}\")")

def list_sectors():
    """
    List available sectors for India market
    """
    sectors_dir = "/Users/chiragpatnaik/Pinescript/tickers/india/sectors"
    
    if not os.path.exists(sectors_dir):
        print("Sectors directory not found")
        return
    
    sectors = [f.replace('.txt', '') for f in os.listdir(sectors_dir) if f.endswith('.txt')]
    sectors.sort()
    
    print("Available sectors for India market:")
    for sector in sectors:
        print(f"  - {sector}")

def main():
    """
    Main function - can be extended for interactive use
    """
    print("Quick Ticker Access Script")
    print("Use the get_tickers() and print_pine_script_format() functions in your code")
    print("\nExample usage:")
    print("  tickers = get_tickers('india', 'subsets', 1)")
    print("  print_pine_script_format('us', 'popular')")

if __name__ == "__main__":
    main()