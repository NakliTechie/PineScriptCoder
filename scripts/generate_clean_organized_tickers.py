#!/usr/bin/env python3
"""
Script to generate clean, organized ticker files (30 active + 10 dummy, alphabetically sorted)
"""

import os
import random

def load_and_sort_tickers(market):
    """Load and sort tickers alphabetically"""
    filepath = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt"
    
    if not os.path.exists(filepath):
        print(f"Ticker file not found: {filepath}")
        return []
    
    with open(filepath, 'r') as f:
        tickers = [line.strip() for line in f if line.strip()]
    
    # Remove duplicates and sort alphabetically
    tickers = sorted(list(set(tickers)))
    return tickers

def create_single_alphabetical_subset(market):
    """Create a single subset of 30 tickers sorted alphabetically"""
    tickers = load_and_sort_tickers(market)
    
    if not tickers:
        return
    
    print(f"Creating alphabetical subset for {market.upper()} market with {len(tickers)} total unique tickers")
    
    # Take first 30 tickers (alphabetically sorted)
    if len(tickers) >= 30:
        selected_tickers = tickers[:30]
    else:
        selected_tickers = tickers.copy()
    
    # Add 10 dummy tickers
    dummy_tickers = ["CRYPTO:BTCUSD"] * 10
    full_list = selected_tickers + dummy_tickers
    
    # Save the subset
    subset_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/alphabetical_30_active.txt"
    with open(subset_file, 'w') as f:
        for ticker in full_list:
            f.write(f"{ticker}\n")
    
    print(f"  Created alphabetical subset: {len(selected_tickers)} active + {len(dummy_tickers)} dummy tickers")
    
    return selected_tickers

def create_random_subsets(market, num_subsets=3, active_tickers=30, dummy_tickers=10):
    """Create a few random subsets of tickers"""
    tickers = load_and_sort_tickers(market)
    
    if not tickers:
        return
    
    print(f"Creating {num_subsets} random subsets for {market.upper()} market")
    
    for i in range(1, num_subsets + 1):
        # Randomly sample active tickers
        if len(tickers) <= active_tickers:
            active_subset = tickers.copy()
        else:
            active_subset = random.sample(tickers, active_tickers)
        
        # Sort alphabetically for consistency
        active_subset.sort()
        
        # Add dummy tickers
        dummy_subset = ["CRYPTO:BTCUSD"] * dummy_tickers
        full_subset = active_subset + dummy_subset
        
        # Save subset
        subset_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/random_{i:02d}_30_active.txt"
        with open(subset_file, 'w') as f:
            for ticker in full_subset:
                f.write(f"{ticker}\n")
        
        print(f"  Created random subset {i}: {len(active_subset)} active + {len(dummy_subset)} dummy tickers")

def create_popular_subset(market):
    """Create a subset of popular/most-traded tickers"""
    if market == "india":
        popular_tickers = [
            "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK",
            "SBIN", "BHARTIARTL", "ITC", "LT", "AXISBANK", "ASIANPAINT",
            "MARUTI", "SUNPHARMA", "TATAMOTORS", "TITAN", "WIPRO", "ULTRACEMCO",
            "M&M", "NESTLEIND", "TECHM", "BAJFINANCE", "ADANIPORTS", "ONGC",
            "POWERGRID", "NTPC", "COALINDIA", "CIPLA", "BPCL", "IOC"
        ][:30]  # Limit to 30
    else:  # US
        popular_tickers = [
            "AAPL", "MSFT", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "BRK.B",
            "JPM", "JNJ", "V", "PG", "UNH", "MA", "DIS", "NVDA", "HD", "BAC",
            "PYPL", "CMCSA", "NFLX", "ADBE", "VZ", "T", "PFE", "XOM", "KO",
            "INTC", "CSCO", "WMT", "ABT", "CRM", "TMO", "PEP", "ABBV", "AVGO"
        ][:30]  # Limit to 30
    
    # Sort alphabetically
    popular_tickers.sort()
    
    # Add dummy tickers
    dummy_tickers = ["CRYPTO:BTCUSD"] * 10
    full_list = popular_tickers + dummy_tickers
    
    # Save popular subset
    popular_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular_30_active.txt"
    with open(popular_file, 'w') as f:
        for ticker in full_list:
            f.write(f"{ticker}\n")
    
    print(f"  Created popular subset: {len(popular_tickers)} active + {len(dummy_tickers)} dummy tickers")

def generate_pine_script_format(market):
    """Generate Pine Script formatted ticker lists"""
    # Process alphabetical subset
    alpha_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/alphabetical_30_active.txt"
    
    if os.path.exists(alpha_file):
        with open(alpha_file, 'r') as f:
            all_tickers = [line.strip() for line in f if line.strip()]
        
        # Generate Pine Script format
        pine_content = f"// {market.upper()} Market Tickers - Alphabetical\n"
        pine_content += f"// Active: 30 tickers, Dummy: 10 tickers (s31-s40)\n\n"
        
        for j, ticker in enumerate(all_tickers, 1):
            # Add exchange prefix for proper TradingView format
            if market == "india":
                if ticker == "CRYPTO:BTCUSD":
                    formatted_ticker = ticker  # Keep crypto as is
                else:
                    formatted_ticker = f"NSE:{ticker}" if not ticker.startswith("NSE:") else ticker
            else:  # US market
                formatted_ticker = ticker  # Keep as is, including crypto dummy
            
            pine_content += f"s{j:02d} = input.symbol(\"{formatted_ticker}\", group = 'Symbols', inline = \"s{j:02d}\")\n"
        
        # Save Pine Script format
        pine_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/alphabetical_30_active.pine"
        with open(pine_file, 'w') as f:
            f.write(pine_content)
        
        print(f"  Generated Pine Script format for alphabetical subset")
    
    # Process popular subset
    popular_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular_30_active.txt"
    
    if os.path.exists(popular_file):
        with open(popular_file, 'r') as f:
            all_tickers = [line.strip() for line in f if line.strip()]
        
        # Generate Pine Script format
        pine_content = f"// {market.upper()} Market Tickers - Popular\n"
        pine_content += f"// Active: 30 tickers, Dummy: 10 tickers (s31-s40)\n\n"
        
        for j, ticker in enumerate(all_tickers, 1):
            # Add exchange prefix for proper TradingView format
            if market == "india":
                if ticker == "CRYPTO:BTCUSD":
                    formatted_ticker = ticker  # Keep crypto as is
                else:
                    formatted_ticker = f"NSE:{ticker}" if not ticker.startswith("NSE:") else ticker
            else:  # US market
                formatted_ticker = ticker  # Keep as is, including crypto dummy
            
            pine_content += f"s{j:02d} = input.symbol(\"{formatted_ticker}\", group = 'Symbols', inline = \"s{j:02d}\")\n"
        
        # Save Pine Script format
        pine_file = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular_30_active.pine"
        with open(pine_file, 'w') as f:
            f.write(pine_content)
        
        print(f"  Generated Pine Script format for popular subset")

def main():
    """Main function to generate clean, organized ticker files"""
    print("Generating clean, organized ticker files (30 active + 10 dummy)...")
    
    # Process both markets
    for market in ["india", "us"]:
        print(f"\nProcessing {market.upper()} market:")
        
        # Create alphabetical subset
        create_single_alphabetical_subset(market)
        
        # Create random subsets
        create_random_subsets(market, num_subsets=3)
        
        # Create popular subset
        create_popular_subset(market)
        
        # Generate Pine Script formats
        generate_pine_script_format(market)
    
    print("\nClean, organized ticker generation complete!")
    print("\nFinal directory structure:")
    print("tickers/")
    print("├── india/")
    print("│   ├── alphabetical_30_active.txt")
    print("│   ├── alphabetical_30_active.pine")
    print("│   ├── popular_30_active.txt")
    print("│   ├── popular_30_active.pine")
    print("│   ├── random_01_30_active.txt")
    print("│   ├── random_02_30_active.txt")
    print("│   ├── random_03_30_active.txt")
    print("│   └── all_tickers.txt")
    print("└── us/")
    print("    ├── alphabetical_30_active.txt")
    print("    ├── alphabetical_30_active.pine")
    print("    ├── popular_30_active.txt")
    print("    ├── popular_30_active.pine")
    print("    ├── random_01_30_active.txt")
    print("    ├── random_02_30_active.txt")
    print("    ├── random_03_30_active.txt")
    print("    └── all_tickers.txt")

if __name__ == "__main__":
    main()