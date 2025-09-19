# Market Tickers - Clean, Organized Structure

This directory contains clean, organized ticker lists for screener development in both Indian and US markets, specifically formatted for the 30 active + 10 dummy ticker pattern.

## Directory Structure

```
tickers/
├── india/
│   ├── alphabetical_30_active.txt    # 30 alphabetically sorted tickers + 10 dummy
│   ├── alphabetical_30_active.pine    # Pine Script formatted version
│   ├── popular_30_active.txt         # 30 popular tickers + 10 dummy
│   ├── popular_30_active.pine         # Pine Script formatted version
│   ├── random_01_30_active.txt        # Random subset 1 (30 active + 10 dummy)
│   ├── random_02_30_active.txt        # Random subset 2 (30 active + 10 dummy)
│   ├── random_03_30_active.txt        # Random subset 3 (30 active + 10 dummy)
│   └── all_tickers.txt              # Complete list of all unique tickers
└── us/
    ├── alphabetical_30_active.txt    # 30 alphabetically sorted tickers + 10 dummy
    ├── alphabetical_30_active.pine    # Pine Script formatted version
    ├── popular_30_active.txt         # 30 popular tickers + 10 dummy
    ├── popular_30_active.pine         # Pine Script formatted version
    ├── random_01_30_active.txt        # Random subset 1 (30 active + 10 dummy)
    ├── random_02_30_active.txt        # Random subset 2 (30 active + 10 dummy)
    ├── random_03_30_active.txt        # Random subset 3 (30 active + 10 dummy)
    └── all_tickers.txt              # Complete list of all unique tickers
```

## Ticker Statistics

### Indian Market
- **Total Unique Tickers**: 219
- **Active Tickers per File**: 30 (alphabetically sorted)
- **Dummy Tickers per File**: 10 (CRYPTO:BTCUSD)
- **Total Tickers per File**: 40

### US Market
- **Total Unique Tickers**: 264
- **Active Tickers per File**: 30 (alphabetically sorted)
- **Dummy Tickers per File**: 10 (CRYPTO:BTCUSD)
- **Total Tickers per File**: 40

## File Types

### Text Files (`*.txt`)
- **Format**: 30 active tickers + 10 dummy tickers
- **Sorting**: Active tickers alphabetically sorted
- **Dummy Tickers**: CRYPTO:BTCUSD (positions 31-40)
- **Purpose**: Easy to read, process, or manually review

### Pine Script Files (`*.pine`)
- **Format**: Ready-to-use Pine Script `input.symbol()` calls
- **Structure**: 
  - s01-s30: Real market tickers with proper exchange prefixes
  - s31-s40: Dummy crypto tickers (CRYPTO:BTCUSD)
- **Grouping**: Proper group and inline parameters for UI organization
- **Prefixes**: NSE: for Indian tickers, no prefix for US tickers
- **Purpose**: Direct copy-paste into screener development

## Usage Recommendations

### For Alphabetical Testing
- **Files**: `alphabetical_30_active.*`
- **Use Case**: Testing with alphabetically sorted tickers
- **Advantage**: Predictable, consistent ordering

### For Popular Stocks
- **Files**: `popular_30_active.*`
- **Use Case**: Testing with well-known, liquid stocks
- **Advantage**: High-volume symbols for reliable data

### For Random Variety
- **Files**: `random_01_30_active.*`, `random_02_30_active.*`, `random_03_30_active.*`
- **Use Case**: Testing with varied market segments
- **Advantage**: Different combinations for diverse testing

## Key Benefits

### Screen Space Optimization
- **30 Active Tickers**: Perfect fit for screen display limitations
- **10 Hidden Dummies**: Maintain 40-ticker structure without clutter
- **Consistent UI**: Same interface across all instances

### Development Efficiency
- **Ready-to-Use**: Pine Script formatted files for direct integration
- **Proper Formatting**: Exchange prefixes and UI parameters included
- **Multiple Options**: Different ticker sets for varied testing needs

### Clean Organization
- **Minimal Files**: Only essential files retained
- **Logical Naming**: Clear file names indicating content and purpose
- **Consistent Structure**: Same format across all files and markets

## Integration Guide

### For Pine Script Development
1. **Choose Ticker Set**: Select appropriate file based on testing needs
2. **Copy Pine Script**: Use `.pine` file for direct copy-paste
3. **Integrate**: Paste into screener code
4. **Note**: Last 10 tickers (s31-s40) are dummy CRYPTO:BTCUSD and should remain disabled

### For Custom Processing
1. **Choose Ticker Set**: Select appropriate `.txt` file
2. **Process**: Read file line by line
3. **Format**: Apply custom formatting as needed
4. **Output**: Generate custom Pine Script or other formats

## Update Process
To regenerate ticker lists with updated source data:
1. Update the source CSV files (`india.csv`, `us.csv`)
2. Run the generation script: `./scripts/generate_clean_organized_tickers.py`
3. All organized files will be automatically regenerated with 30 active + 10 dummy structure