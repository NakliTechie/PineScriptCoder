# Pine Script Development Instructions

## Project Organization

### Directory Structure
```
Pinescript/
├── guidelines/                 # Development guidelines and rules
├── pine_script_references/     # Official reference documentation (v3-v6)
├── scripts/                    # Utility scripts for reference management
├── from_scratch/               # New development from scratch
├── improve_existing/           # Enhancement of existing code
├── screeners/                  # Screener development
├── templates/                  # Code templates for common patterns
├── documentation/              # User documentation and notes
└── README.md                   # Project overview and instructions
```

## Root Directory Management

### Keep Root Clean
1. **Only essential files in root**:
   - Main project README.md
   - High-level documentation
   - Project configuration files

2. **All development work in subdirectories**:
   - New development in `from_scratch/`
   - Code improvements in `improve_existing/`
   - Screeners in `screeners/`
   - Templates in `templates/`
   - Documentation in `documentation/`

3. **Reasoning**:
   - Maintains clear project structure
   - Easy to navigate and find specific files
   - Prevents clutter and confusion
   - Facilitates version control and sharing

## Development Workflows by Type

### 1. From Scratch Development (`from_scratch/`)
**Purpose**: Creating new indicators, strategies, or tools from nothing

**Workflow**:
1. **Planning**:
   - Define requirements and objectives
   - Identify needed Pine Script functions (reference `pine_script_references/`)
   - Check guidelines in `guidelines/` directory

2. **Development**:
   - Start with template from `templates/` if available
   - Develop in `from_scratch/` directory
   - Use incremental development with frequent testing
   - Follow coding standards from `guidelines/`

3. **Testing**:
   - Test on multiple assets and timeframes
   - Validate logic and calculations
   - Check for syntax errors using guidelines

4. **Completion**:
   - Add required header to script
   - Document functionality and usage
   - Move to final location when complete

### 2. Improve Existing Code (`improve_existing/`)
**Purpose**: Taking existing Pine Script code and enhancing it

**Workflow**:
1. **Analysis**:
   - Place original code in `improve_existing/`
   - Review code for understanding
   - Identify improvement opportunities
   - Check against guidelines for violations

2. **Planning**:
   - Define specific improvements needed
   - Prioritize changes (performance, readability, functionality)
   - Plan implementation approach

3. **Implementation**:
   - Create new version with clear versioning
   - Make incremental improvements
   - Document each change
   - Preserve original for reference

4. **Validation**:
   - Verify improved code produces same results where expected
   - Test new functionality
   - Ensure no guideline violations

### 3. Screener Development (`screeners/`)
**Purpose**: Creating market scanning tools for TradingView

**Workflow**:
1. **Criteria Definition**:
   - Define screening criteria and conditions
   - Identify required data and functions
   - Plan output format (alerts, tables, etc.)

2. **Development**:
   - Develop in `screeners/` directory
   - Implement screening logic
   - Create appropriate outputs (plotshapes, alerts, etc.)
   - Follow screener-specific best practices

3. **Testing**:
   - Test with various market conditions
   - Validate screening accuracy
   - Optimize for performance

4. **Deployment**:
   - Document screening criteria
   - Provide usage instructions
   - Optimize for TradingView environment

## Development Process

### 1. New Script Development
1. Start with template from `templates/`
2. Develop in appropriate directory based on type:
   - `from_scratch/` for new development
   - `improve_existing/` for code enhancement
   - `screeners/` for market screeners
3. Move to appropriate final directory when complete

### 2. Code Quality Process
1. Follow guidelines in `guidelines/` directory
2. Reference official documentation in `pine_script_references/`
3. Validate syntax before delivery
4. Include required header in all new scripts
5. Check for common mistakes (see quick reference)

### 3. File Management
1. Use descriptive file names
2. Include version numbers for iterations
3. Document significant changes
4. Remove temporary/intermediate files

## Naming Conventions

### Files
- Use snake_case: `moving_average_indicator.pine`
- Include version if applicable: `rsi_screener_v2.pine`
- Be descriptive but concise
- Include type identifier when helpful: `screener_`, `indicator_`, `strategy_`

### Directories
- Use lowercase plural names: `indicators/`, `screeners/`
- Match the organizational structure above

## Version Control Preparation

### Ready for Git
1. Clean root directory
2. Logical subdirectory structure
3. Consistent naming conventions
4. Clear documentation
5. No temporary or intermediate files

## Screener-Specific Development Guidelines

### Automated Screener Generation Process

#### Standard Configuration
All screeners follow a 30+10 configuration:
- **30 active tickers** (positions 1-30): Market-specific tickers, all enabled
- **10 padding tickers** (positions 31-40): Commodity/crypto tickers, all disabled

#### Market-Specific Padding Strategies
1. **US Market**: Positions 31-40 filled with crypto tickers (FILUSDT, HOTUSDT, etc.)
2. **India Market**: Positions 31-40 filled with commodity stocks + crypto tickers (JSWSTEEL, OIL, BTCUSD, etc.)

#### Handling Incomplete Instances
When there are insufficient tickers for complete instances:
1. **Partial Instance**: Use remaining market tickers + fill gaps with global commodities
2. **Global Commodity Tickers**: Diverse assets including:
   - Precious metals (XAUUSD, XAGUSD)
   - Industrial metals (HGUSD)
   - Energy (USOIL, CLUSD)
   - Major currencies (EURUSD, GBPUSD)
   - Crypto currencies (BTCUSD, ETHUSD)
3. **Duplicate Instances**: Copy the partial instance (now containing global commodities)

#### Benefits of Global Commodity Padding
- **Eliminates Redundancy**: No duplicate tickers in later screeners
- **Improves Diversification**: Global commodities provide exposure to different asset classes
- **Enhances Coverage**: Broader market representation in incomplete instances
- **Maintains Structure**: Still follows the 30+10 configuration
- **Market Relevance**: Global commodities are relevant regardless of local market conditions

#### Generator Script Usage
The framework includes generator scripts for creating screener instances with proper ticker distribution.

Example usage:
```bash
python3 screener_generator.py <market> <num_instances> <base_script_name> <script_title>
```

The generator automatically:
- Reads market tickers from `/tickers/{market}/all_tickers.txt`
- Applies market-specific padding strategies
- Uses global commodities for incomplete instances
- Sets appropriate enable flags
- Generates consistent 40-position screeners

## Future Expansion

### Adding New Categories
1. Create new subdirectory in root
2. Update this README with description
3. Maintain consistent structure
4. Document purpose and usage

### Reference Updates
1. Keep `pine_script_references/` updated
2. Maintain all versions (v3-v6)
3. Preserve organization structure
4. Update documentation as needed