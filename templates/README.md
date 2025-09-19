# Pine Script Templates

This directory contains templates for different types of Pine Script development to help you get started quickly.

## Template Types

### 1. Indicator Template (`indicator_template.pine`)
- Use for creating new visualization indicators
- Includes basic structure with inputs, calculations, and plotting
- Ready for overlay=true indicators

### 2. Strategy Template (`strategy_template.pine`)
- Use for creating new trading strategies
- Includes strategy framework with entry/exit logic
- Pre-configured with basic strategy settings

### 3. Screener Template (`screener_template.pine`)
- Use for creating market screening tools
- Designed for non-overlay indicators
- Includes structure for screening criteria and outputs

### 4. Improvement Template (`improvement_template.pine`)
- Use when enhancing existing code
- Includes documentation sections for tracking changes
- Structured for incremental improvements

### 5. Gold Standard Screener Template (`gold_standard_screener_template.pine`)
- Based on your reference examples (screener_ex1.txt, screener_ex10.txt)
- Multi-instance architecture with position control
- Supports up to 40 symbols with enable flags
- Color-coded signal display with table formatting
- Follows the TRIP screener pattern

### 6. HTI Screener Example (`hti_screener_example.pine`)
- Specific implementation based on your TRIP screener
- Demonstrates proper function structure with helpers
- Shows the T3 calculation and HTI signal logic
- Ready-to-use example with 5 symbols

## How to Use

1. **Copy the appropriate template**:
   ```bash
   # For new indicators
   cp templates/indicator_template.pine from_scratch/my_new_indicator.pine
   
   # For improving existing code
   cp templates/improvement_template.pine improve_existing/enhanced_version.pine
   
   # For screeners (using gold standard)
   cp templates/gold_standard_screener_template.pine screeners/my_screener.pine
   ```

2. **Rename the file** to reflect your specific development

3. **Modify the content** according to your needs:
   - Replace `{{SCRIPT_NAME}}` and `{{SCREEN_NUMBER}}` placeholders
   - Add your specific strategy parameters
   - Implement your signal calculation logic
   - Customize symbol list as needed

4. **Follow the TODO comments** to implement your logic

5. **Test thoroughly** before finalizing

## Gold Standard Screener Specific Instructions

### Key Features:
- **Multi-instance support**: Create up to 10 instances with different `scr_numb` values
- **Position control**: `scr_numb` controls horizontal positioning (1 = rightmost)
- **Symbol management**: 40 symbols with individual enable flags
- **Color coding**: BUY (green), SELL (red), NONE (gray)
- **Dynamic display**: Table adjusts based on screen number

### Customization Points:
1. **Script Name**: Update `SCRIPT_NAME` variable and indicator title
2. **Screen Number**: Set `scr_numb` input to desired position (1-10)
3. **Symbol List**: Modify the 40 symbol inputs to your preferred tickers
4. **Strategy Logic**: Implement your signal calculation in `calculateSignal()` function
5. **Helper Functions**: Add helper functions at the top level (never inside other functions)
6. **Parameters**: Add strategy-specific inputs in the parameters section

### Function Structure Guidelines:
- **Define all helper functions at the top level** (never inside other functions)
- **Create one main calculation function** that calls helper functions
- **Use the `=>` syntax** for function definitions
- **Return a standardized signal string** ("BUY", "SELL", "---")

### Deployment:
1. Create instance 1 with `scr_numb = 1` (rightmost position)
2. Create additional instances with increasing `scr_numb` values
3. Each instance can have different symbol lists if needed
4. All instances share the same underlying logic

## Best Practices

- Always include the required license header
- Follow naming conventions (snake_case)
- Document your code with comments
- Test on multiple timeframes and assets
- Validate against guidelines in `guidelines/` directory
- Define all functions at top level (no nested functions)