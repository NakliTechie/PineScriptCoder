# Pine Script Development Framework

This is a comprehensive Pine Script development framework with organized references, guidelines, and development tools for creating TradingView indicators, strategies, and screeners. This framework was created using [Qwen Code](https://github.com/QwenLM/qwen-code). You can find this project on [GitHub](https://github.com/NakliTechie/PineScriptCoder).

## Project Overview

This framework provides a structured approach to Pine Script development with organized references, guidelines, and development tools. It includes templates, tickers, and utility scripts to accelerate the development process.

## Project Structure

```
├── Development_Framework/          # Framework components
│   ├── checkpoint_system/          # Progress tracking and resume capability
│   │   ├── checkpoint_*.json         # Timestamped checkpoint files
│   │   ├── latest_checkpoint.json    # Symlink to most recent checkpoint
│   │   ├── template_checkpoint.json  # Template for new checkpoints
│   │   ├── README.md                # Checkpoint system documentation
│   │   └── DEVELOPMENT_GUIDE.md     # Detailed usage guide
│   └── README.md                   # Framework documentation
├── guidelines/                     # Development guidelines and rules
│   ├── original_guidelines.txt     # Original guidelines
│   ├── pine_script_guidelines.json # Structured guidelines (JSON)
│   ├── pine_script_guidelines.md   # Structured guidelines (Markdown)
│   └── pine_script_quick_reference.txt # Quick reference guide
├── pine_script_references/         # Official Pine Script reference (v3-v6)
│   ├── v3/                         # Version 3 reference
│   ├── v4/                         # Version 4 reference
│   ├── v5/                         # Version 5 reference
│   ├── v6/                         # Version 6 reference
│   ├── OVERALL_SUMMARY.md          # Comparison of all versions
│   └── README.md                   # Overview of all references
├── screeners/                      # Screener development organized by type
│   ├── example_screener/           # Example screener implementation
│   │   ├── wip/                    # Work-in-progress development
│   │   ├── final/                  # Final production version
│   │   └── README.md              # Example screener documentation
│   ├── multi_column/              # Multi-column screeners by information density
│   │   ├── wip/                    # Work-in-progress development
│   │   ├── final/                  # Final production versions
│   │   └── README.md              # Multi-column screener documentation
│   └── README.md                  # Screeners overview
├── scripts/                       # Utility scripts for development
│   ├── checkpoint_manager.py        # Checkpoint management system
│   ├── simple_checkpoint.py        # Simple checkpoint utility
│   ├── convert_to_pdf.py           # Convert Pine Script reference to PDF
│   ├── organize_pine_reference.py  # Organize Pine Script reference materials
│   ├── parse_all_versions.py       # Parse all Pine Script versions
│   ├── parse_toc.py                # Parse table of contents
│   ├── pineref2pdf.py              # Convert Pine Script reference to PDF
│   ├── scrape_all_versions.py      # Scrape all Pine Script versions
│   ├── scrape_pine_reference.py    # Scrape Pine Script reference
│   └── scrape_pine_reference_selenium.py # Scrape Pine Script reference with Selenium
├── templates/                     # Code templates for different development types
│   ├── gold_standard_screener_template.pine # Multi-instance screener template
│   ├── indicator_template.pine    # New indicator development template
│   ├── strategy_template.pine     # New strategy development template
│   ├── screener_template.pine      # New screener development template
│   ├── improvement_template.pine  # Code improvement template
│   └── README.md                  # Template usage documentation
├── tickers/                       # Market tickers organized for screener development
│   ├── india/                     # Indian market tickers (30 active + 10 dummy)
│   │   ├── alphabetical_30_active.txt  # Alphabetically sorted tickers
│   │   ├── alphabetical_30_active.pine  # Pine Script formatted version
│   │   ├── popular_30_active.txt       # Popular tickers
│   │   ├── popular_30_active.pine       # Pine Script formatted version
│   │   ├── random_01_30_active.txt      # Random subset 1
│   │   ├── random_02_30_active.txt      # Random subset 2
│   │   ├── random_03_30_active.txt       # Random subset 3
│   │   └── all_tickers.txt              # Complete list of all unique tickers
│   ├── us/                        # US market tickers (30 active + 10 dummy)
│   │   ├── alphabetical_30_active.txt  # Alphabetically sorted tickers
│   │   ├── alphabetical_30_active.pine  # Pine Script formatted version
│   │   ├── popular_30_active.txt       # Popular tickers
│   │   ├── popular_30_active.pine       # Pine Script formatted version
│   │   ├── random_01_30_active.txt      # Random subset 1
│   │   ├── random_02_30_active.txt      # Random subset 2
│   │   ├── random_03_30_active.txt       # Random subset 3
│   │   └── all_tickers.txt              # Complete list of all unique tickers
│   └── README.md                 # Tickers organization documentation
├── from_scratch/                  # New development from scratch
├── improve_existing/              # Enhancement of existing code
├── atr_retracement_ema_signals.pine   # EMA signals example
├── atr_retracement_ema_strategy.pine  # EMA strategy example
└── README.md                          # Main project overview
```

## Key Development Commands

- **Test single instance**: Copy screener code to TradingView editor
- **Update Pine Script references**: `python scripts/scrape_all_versions.py`
- **Organize references**: `python scripts/organize_pine_reference.py`

## Pine Script Development Guidelines

### Project Context
- **Purpose**: Developing Pine Script indicators and screeners for TradingView
- **Primary User**: Trader using Pine Script on TradingView

### Code Style Requirements
1. Do not use semicolons (`;`) instead of line breaks - this is illegal in Pine Script
2. Do not use backslashes (`\`) to continue long statements on another line - this is illegal in Pine Script
3. Do not use plus (`+`) to break lines into a new line - this is illegal in Pine Script
4. Use proper indentation for `if`, `else`, `else if` statements - Pine Script is very finicky about indentation
5. Be judicious in the use of curly braces `{}` - Pine Script mostly uses regular parentheses `()`
6. Don't use too many levels of nesting

### Function Usage
1. Do not use `ta.sum` - it does not exist in the reference; always use `math.sum`
2. Use `alert()` instead of `alertcondition()`
3. `nz()` can only be used for `int`/`float` types, not for `bool` and `text`
4. For `request.security()` function, use proper lookahead parameter:
   - Correct: `lookahead = barmerge.lookahead_off` or `lookahead = barmerge.lookahead_on`
   - Incorrect: `lookahead=false` or `lookahead=true`

### Scope Restrictions
1. `plotshape` cannot be used in local scope (inside an `if` statement)
2. You cannot define functions using the shorthand `=>` syntax inside another function block - create a helper function outside the function loop and call it instead

### Naming Conventions
1. Symbol names cannot have special characters - if they exist, they need to be replaced with underscores (`_`)

### Code Delivery Preferences
1. Return efficient code optimized for TradingView
2. If the return code is long, unless specifically asked, return snippets with the previous line/section so that it is easy to do a search and replace
3. Always use a light touch with minimal changes instead of large rewrites
4. Large rewrites only if specifically requested
5. When writing new indicators or full code for copy-paste, incorporate the required license header

### Required Header
For new indicators, always include:
```
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PineScript Development Framework
```

## Checkpoint System
- Track progress with JSON checkpoint files
- Create checkpoints after major tasks
- Resume work using `latest_checkpoint.json`
- Document next steps and current focus in each checkpoint

## Pine Script Reference Management

This framework includes powerful Python tools for managing Pine Script references:

- **Automatic Scraping**: Download the latest Pine Script references directly from TradingView
- **Multi-Version Support**: Support for Pine Script v3, v4, v5, and v6
- **Organization Tools**: Automatically organize references by categories (functions, variables, etc.)
- **PDF Conversion**: Convert references to PDF for offline reading
- **Regular Updates**: Keep your references current with automated tools

To update your Pine Script references:
```bash
# Scrape all versions
python scripts/scrape_all_versions.py

# Organize references
python scripts/organize_pine_reference.py
```