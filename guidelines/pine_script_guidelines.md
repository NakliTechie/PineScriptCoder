# Pine Script Development Guidelines

## Project Context
- **Purpose**: Developing Pine Script indicators and screeners for TradingView
- **Primary User**: Trader using Pine Script on TradingView

## Coding Standards

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

## Code Delivery Preferences
1. Return efficient code optimized for TradingView
2. If the return code is long, unless specifically asked, return snippets with the previous line/section so that it is easy to do a search and replace
3. Always use a light touch with minimal changes instead of large rewrites
4. Large rewrites only if specifically requested
5. When writing new indicators or full code for copy-paste, incorporate the required license header

## Quality Assurance Checklist
Before posting any code, always:
1. Do a pre-check of the syntax
2. Verify what is allowed vs. illegal in Pine Script
3. Refer to the above list of rules during code review
4. Refer to system instructions after every user input

## Required Header
For new indicators, always include:
```
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PineScript Development Framework
```