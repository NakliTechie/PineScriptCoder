# Pine Script Development Framework

This repository contains a complete framework for Pine Script development with organized references, guidelines, and development tools.

## Directory Structure

```
├── checkpoints/                  # Progress tracking and resume capability
│   ├── checkpoint_*.json           # Timestamped checkpoint files
│   ├── latest_checkpoint.json      # Symlink to most recent checkpoint
│   ├── template_checkpoint.json    # Template for new checkpoints
│   ├── README.md                  # Checkpoint system documentation
│   └── DEVELOPMENT_GUIDE.md       # Detailed usage guide
├── guidelines/                    # Development guidelines and rules
│   ├── original_guidelines.txt     # Original guidelines from user
│   ├── pine_script_guidelines.json # Structured guidelines (JSON)
│   ├── pine_script_guidelines.md   # Structured guidelines (Markdown)
│   └── pine_script_quick_reference.txt # Quick reference guide
├── pine_script_references/        # Official Pine Script reference (v3-v6)
│   ├── v3/                         # Version 3 reference
│   ├── v4/                         # Version 4 reference
│   ├── v5/                         # Version 5 reference
│   ├── v6/                         # Version 6 reference
│   ├── OVERALL_SUMMARY.md          # Comparison of all versions
│   └── README.md                   # Overview of all references
├── screeners/                     # Screener development organized by type
│   ├── hti_screener/              # HTI (Hull T3 Indicator) screener - 10 instance deployment
│   │   ├── wip/                    # Work-in-progress development
│   │   ├── final/                  # Final production instances (1-10)
│   │   └── README.md              # HTI screener documentation
│   ├── multi_column/              # Multi-column screeners by information density
│   │   ├── wip/                    # Work-in-progress development
│   │   ├── final/                  # Final production versions
│   │   └── README.md              # Multi-column screener documentation
│   ├── wip/                        # General work-in-progress files
│   ├── DEVELOPMENT_WORKFLOW.md     # Step-by-step development process
│   ├── OPERATING_GUIDE.md          # Technical implementation details
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
│   ├── hti_screener_example.pine  # HTI screener concrete example
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
└── README.md                      # Main project overview
```

## Key Features

### 1. **Comprehensive References**
- **All Pine Script Versions**: Organized documentation for v3, v4, v5, and v6
- **Easy Navigation**: Categorized by functions, variables, constants, etc.
- **Version Comparison**: Track evolution of Pine Script features

### 2. **Development Guidelines**
- **Coding Standards**: Rules for Pine Script syntax and style
- **Common Mistakes**: Quick reference to avoid illegal operations
- **Best Practices**: Efficient code delivery preferences

### 3. **Screener Development Framework**
- **HTI Screener**: Multi-instance architecture with 10 positions
- **Multi-Column**: Information density focused screeners
- **Workflow**: Structured development process from WIP to production
- **Templates**: Ready-to-use code templates for different development types

### 4. **Market Tickers**
- **Indian Market**: 219 unique tickers organized for screener development
- **US Market**: 264 unique tickers organized for screener development
- **Optimized Format**: 30 active tickers + 10 dummy tickers per instance
- **Pine Script Ready**: Pre-formatted `input.symbol()` calls
- **Multiple Options**: Alphabetical, popular, and random ticker sets

### 5. **Checkpoint System**
- **Progress Tracking**: Automatic progress tracking for development tasks
- **Resume Capability**: Seamless continuation after interruptions
- **State Preservation**: Maintain context of ongoing work
- **Workflow Documentation**: Record completed tasks and next steps

### 6. **Clean Organization**
- **Minimal Clutter**: Only essential files and directories retained
- **Logical Structure**: Easy navigation and maintenance
- **Consistent Formatting**: Standardized across all components

## Development Workflow

### 1. **Reference Materials**
Access organized Pine Script documentation in `pine_script_references/`

### 2. **Guidelines**
Follow coding standards in `guidelines/` directory

### 3. **Screener Development**
- **Work in Progress**: Develop in appropriate `wip/` directory
- **Test in TradingView**: Copy code for validation and refinement
- **Production Deployment**: Move finalized logic to `final/` directories

### 4. **Ticker Integration**
- **Choose Market**: Select `india/` or `us/` tickers
- **Choose Type**: Alphabetical, popular, or random ticker sets
- **Integrate**: Use Pine Script formatted files for direct copy-paste
- **Optimize**: 30 active + 10 dummy structure fits screen space perfectly

### 5. **Progress Tracking**
- **Create Checkpoints**: Use checkpoint system to track progress
- **Resume Work**: Easily continue from last interruption point
- **Document Steps**: Record completed tasks and next actions

## Usage Instructions

### For New Development
1. Review guidelines in `guidelines/` directory
2. Browse references in `pine_script_references/` for function details
3. Choose appropriate screener template from `templates/` directory
4. Select tickers from `tickers/` directories based on market focus
5. Develop in WIP directories, test in TradingView
6. Deploy to final directories when ready
7. Create checkpoints to track progress

### For Ticker Integration
1. Choose market (`india/` or `us/`)
2. Select appropriate ticker set:
   - `alphabetical_30_active.*` for alphabetically sorted tickers
   - `popular_30_active.*` for well-known stocks
   - `random_*_30_active.*` for varied combinations
3. Use Pine Script formatted files for direct integration
4. Copy-paste into screener code
5. Last 10 tickers (s31-s40) will be disabled by default

### For Progress Tracking
1. **Initialize**: Create initial checkpoint for new project
2. **Update**: Create checkpoints after completing subtasks
3. **Resume**: Use latest checkpoint to continue interrupted work
4. **Track**: Monitor overall progress throughout development

## Key Benefits

### 1. **Organized Structure**
- Clear separation of concerns
- Logical directory hierarchy
- Easy navigation and maintenance

### 2. **Ready-to-Use Resources**
- Pre-formatted Pine Script code
- Optimized ticker lists (30 active + 10 dummy)
- Multi-instance screener templates

### 3. **Efficient Development**
- Follow proven workflows
- Leverage existing templates
- Integrate tickers with minimal effort

### 4. **Interruptible Workflow**
- Automatic progress tracking
- Seamless resume capability
- State preservation across sessions

### 5. **Scalable Organization**
- Accommodates multiple screener types
- Supports different market focuses
- Flexible for future expansion

## Maintenance

### Regular Updates
- **Ticker Lists**: Regenerate when source CSVs change
- **References**: Update when Pine Script versions change
- **Checkpoints**: Review and archive completed projects
- **Templates**: Update with improved patterns and practices

### Backup Strategy
- **Version Control**: Include repository in Git or other VCS
- **Cloud Storage**: Sync to cloud storage for redundancy
- **Automated Backups**: Schedule regular backups of key directories