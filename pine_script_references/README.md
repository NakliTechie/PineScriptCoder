# Pine Script References - Complete Documentation Set

This repository contains organized references for all versions of Pine Script (v3, v4, v5, and v6) as documented on TradingView's official reference pages.

## Folder Structure

```
pine_script_references/
├── v3/                     # Pine Script Version 3
│   ├── README.md           # Overview of v3 reference
│   ├── categories/         # Organized by category
│   │   ├── functions.md
│   │   ├── variables.md
│   │   ├── constants.md
│   │   ├── keywords.md
│   │   └── operators.md
│   └── table_of_contents.html  # Original TOC from TradingView
├── v4/                     # Pine Script Version 4
│   ├── README.md           # Overview of v4 reference
│   ├── categories/         # Organized by category
│   │   ├── functions.md
│   │   ├── variables.md
│   │   ├── constants.md
│   │   ├── keywords.md
│   │   ├── types.md
│   │   └── operators.md
│   └── table_of_contents.html  # Original TOC from TradingView
├── v5/                     # Pine Script Version 5
│   ├── README.md           # Overview of v5 reference
│   ├── categories/         # Organized by category
│   │   ├── functions.md
│   │   ├── variables.md
│   │   ├── constants.md
│   │   ├── keywords.md
│   │   ├── types.md
│   │   ├── operators.md
│   │   └── annotations.md
│   └── table_of_contents.html  # Original TOC from TradingView
├── v6/                     # Pine Script Version 6
│   ├── README.md           # Overview of v6 reference
│   ├── categories/         # Organized by category
│   │   ├── functions.md
│   │   ├── variables.md
│   │   ├── constants.md
│   │   ├── keywords.md
│   │   ├── types.md
│   │   ├── operators.md
│   │   └── annotations.md
│   └── table_of_contents.html  # Original TOC from TradingView
├── OVERALL_SUMMARY.md      # Summary of all versions
└── SUMMARY.md             # Original summary file
```

## Statistics

| Version | Categories | Functions | Variables | Constants | Properties | Total Items |
|---------|------------|-----------|-----------|-----------|------------|-------------|
| v3      | 5          | 113       | 45        | 109       | 150        | 304         |
| v4      | 6          | 269       | 58        | 183       | 260        | 569         |
| v5      | 7          | 452       | 98        | 198       | 318        | 866         |
| v6      | 7          | 457       | 107       | 235       | 346        | 915         |

## Categories

Each version contains the following types of categories:

1. **Functions** - Built-in functions like `sma()`, `ema()`, `plot()`, etc.
2. **Variables** - Built-in variables like `close`, `open`, `high`, `low`, etc.
3. **Constants** - Built-in constants like `color.red`, `na`, etc.
4. **Keywords** - Language keywords like `var`, `if`, `for`, etc.
5. **Types** - Data types like `int`, `float`, `bool`, `color`, etc. (v4+)
6. **Operators** - Operators like `+`, `-`, `*`, `/`, `and`, `or`, etc.
7. **Annotations** - Annotations like `@overlay`, `@resolution`, etc. (v5+)

## How to Use

1. **Browse by Version**: Each version directory contains a README.md file that lists all categories and their contents.

2. **Browse by Category**: Within each version's `categories/` directory, you'll find markdown files organized by category.

3. **Search**: Use your system's file search or grep to find specific functions or variables.

## Converting to PDF

If you have the necessary tools installed, you can convert the markdown files to PDF:

1. **Using Pandoc**:
   ```bash
   pandoc README.md -o reference.pdf --pdf-engine=xelatex
   ```

2. **Using markdown-pdf**:
   ```bash
   markdown-pdf README.md -o reference.pdf
   ```

## Source

All content was extracted from TradingView's official Pine Script reference pages:
- https://www.tradingview.com/pine-script-reference/v3/
- https://www.tradingview.com/pine-script-reference/v4/
- https://www.tradingview.com/pine-script-reference/v5/
- https://www.tradingview.com/pine-script-reference/v6/

## Notes

- This is an unofficial extraction of publicly available documentation
- All content remains the property of TradingView
- This organization is meant to make the reference more accessible and easier to navigate
- The extraction was done using automated tools to preserve the original structure and content