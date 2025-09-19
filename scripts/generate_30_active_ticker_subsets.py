#!/usr/bin/env python3
"""
Script to generate ticker subsets for screener instances (30 active + 10 dummy)
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
    
    # Remove duplicates and sort
    tickers = sorted(list(set(tickers)))
    return tickers

def generate_subsets(market, num_subsets=10, active_tickers=30, dummy_tickers=10):
    """Generate subsets of tickers for different screener instances (30 active + 10 dummy)"""
    tickers = load_tickers(market)
    
    if not tickers:
        return
    
    print(f"Generating {num_subsets} subsets for {market.upper()} market with {len(tickers)} total unique tickers")
    print(f"  Active tickers: {active_tickers}, Dummy tickers: {dummy_tickers}")
    
    # Create directory for subsets
    subsets_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/subsets_30_active"
    os.makedirs(subsets_dir, exist_ok=True)
    
    # Generate subsets
    for i in range(1, num_subsets + 1):
        # Randomly sample active tickers
        if len(tickers) <= active_tickers:
            active_subset = tickers.copy()
        else:
            active_subset = random.sample(tickers, active_tickers)
        
        # Sort for consistency
        active_subset.sort()
        
        # Create dummy tickers (same for all instances to save space)
        if market == "india":
            dummy_tickers_list = ["CRYPTO:BTCUSD"] * dummy_tickers
        else:  # US market
            dummy_tickers_list = ["CRYPTO:BTCUSD"] * dummy_tickers
        
        # Combine active and dummy tickers
        full_subset = active_subset + dummy_tickers_list
        
        # Save subset
        subset_file = f"{subsets_dir}/subset_{i:02d}.txt"
        with open(subset_file, 'w') as f:
            for ticker in full_subset:
                f.write(f"{ticker}\n")
        
        print(f"  Generated subset {i}: {len(active_subset)} active + {len(dummy_tickers_list)} dummy tickers")
    
    # Also create a version with only active tickers for reference
    active_only_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/active_only"
    os.makedirs(active_only_dir, exist_ok=True)
    
    for i in range(1, num_subsets + 1):
        # Randomly sample active tickers
        if len(tickers) <= active_tickers:
            active_subset = tickers.copy()
        else:
            active_subset = random.sample(tickers, active_tickers)
        
        # Sort for consistency
        active_subset.sort()
        
        # Save active-only subset
        subset_file = f"{active_only_dir}/active_only_{i:02d}.txt"
        with open(subset_file, 'w') as f:
            for ticker in active_subset:
                f.write(f"{ticker}\n")
        
        print(f"  Generated active-only subset {i}: {len(active_subset)} tickers")

def generate_pine_script_format(market):
    """Generate Pine Script formatted ticker lists (30 active + 10 dummy)"""
    subsets_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/subsets_30_active"
    
    if not os.path.exists(subsets_dir):
        print(f"Subsets directory not found: {subsets_dir}")
        return
    
    pine_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/pine_script_30_active"
    os.makedirs(pine_dir, exist_ok=True)
    
    # Process each subset
    for i in range(1, 11):
        subset_file = f"{subsets_dir}/subset_{i:02d}.txt"
        
        if not os.path.exists(subset_file):
            continue
        
        with open(subset_file, 'r') as f:
            all_tickers = [line.strip() for line in f if line.strip()]
        
        # Generate Pine Script format
        pine_content = f"// {market.upper()} Market Tickers - Instance {i}\n"
        pine_content += f"// Active: 30 tickers, Dummy: 10 tickers\n\n"
        
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
        pine_file = f"{pine_dir}/tickers_instance_{i:02d}.pine"
        with open(pine_file, 'w') as f:
            f.write(pine_content)
        
        print(f"  Generated Pine Script format for instance {i} (30 active + 10 dummy)")

def create_popular_subsets_30(market):
    """Create subsets of 30 popular/most-traded tickers"""
    if market == "india":
        # For India, use common large-cap stocks (limited to 30)
        popular_tickers = [
            "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK",
            "SBIN", "BHARTIARTL", "ITC", "LT", "AXISBANK", "ASIANPAINT",
            "MARUTI", "SUNPHARMA", "TATAMOTORS", "TITAN", "WIPRO", "ULTRACEMCO",
            "M&M", "NESTLEIND", "TECHM", "BAJFINANCE", "ADANIPORTS", "ONGC",
            "POWERGRID", "NTPC", "COALINDIA", "CIPLA", "BPCL", "IOC"
        ][:30]  # Limit to 30
    else:  # US
        # For US, common large-cap stocks (limited to 30)
        popular_tickers = [
            "AAPL", "MSFT", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "BRK.B",
            "JPM", "JNJ", "V", "PG", "UNH", "MA", "DIS", "NVDA", "HD", "BAC",
            "PYPL", "CMCSA", "NFLX", "ADBE", "VZ", "T", "PFE", "XOM", "KO",
            "INTC", "CSCO", "WMT", "ABT", "CRM", "TMO", "PEP", "ABBV", "AVGO",
            "ACN", "TXN", "COST", "DHR"
        ][:30]  # Limit to 30
    
    # Save popular tickers subset (30 active + 10 dummy)
    popular_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular_30_active"
    os.makedirs(popular_dir, exist_ok=True)
    
    # Create full list (30 active + 10 dummy)
    full_list = popular_tickers + ["CRYPTO:BTCUSD"] * 10
    
    popular_file = f"{popular_dir}/popular_tickers_30_active.txt"
    with open(popular_file, 'w') as f:
        for ticker in full_list:
            f.write(f"{ticker}\n")
    
    # Also save active-only version
    active_only_file = f"{popular_dir}/popular_tickers_active_only.txt"
    with open(active_only_file, 'w') as f:
        for ticker in popular_tickers:
            f.write(f"{ticker}\n")
    
    print(f"  Created popular tickers subset: {len(popular_tickers)} active + 10 dummy tickers")
    
    # Generate Pine Script format
    pine_dir = f"/Users/chiragpatnaik/Pinescript/tickers/{market}/popular_30_active/pine_script"
    os.makedirs(pine_dir, exist_ok=True)
    
    pine_content = f"// {market.upper()} Popular Tickers (30 active + 10 dummy)\n"
    pine_content += f"// Active: {len(popular_tickers)} tickers, Dummy: 10 tickers\n\n"
    
    for j, ticker in enumerate(full_list, 1):
        # Add exchange prefix for proper TradingView format
        if market == "india":
            if ticker == "CRYPTO:BTCUSD":
                formatted_ticker = ticker  # Keep crypto as is
            else:
                formatted_ticker = f"NSE:{ticker}" if not ticker.startswith("NSE:") else ticker
        else:  # US market
            formatted_ticker = ticker  # Keep as is, including crypto dummy
        
        pine_content += f"s{j:02d} = input.symbol(\"{formatted_ticker}\", group = 'Symbols', inline = \"s{j:02d}\")\n"
    
    pine_file = f"{pine_dir}/popular_tickers.pine"
    with open(pine_file, 'w') as f:
        f.write(pine_content)
    
    print(f"  Generated Pine Script format for popular tickers")

def main():
    """Main function to generate all ticker subsets with 30 active + 10 dummy"""
    print("Generating ticker subsets (30 active + 10 dummy) for screener development...")
    
    # Generate subsets for both markets
    for market in ["india", "us"]:
        print(f"\nProcessing {market.upper()} market:")
        generate_subsets(market, active_tickers=30, dummy_tickers=10)
        generate_pine_script_format(market)
        create_popular_subsets_30(market)
    
    print("\nTicker subset generation complete!")
    print("\nDirectory structure:")
    print("tickers/")
    print("├── india/")
    print("│   ├── subsets_30_active/")
    print("│   ├── active_only/")
    print("│   ├── popular_30_active/")
    print("│   └── pine_script_30_active/")
    print("└── us/")
    print("    ├── subsets_30_active/")
    print("    ├── active_only/")
    print("    ├── popular_30_active/")
    print("    └── pine_script_30_active/")

if __name__ == "__main__":
    main()