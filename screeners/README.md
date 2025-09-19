# Screeners

This directory contains Pine Script screeners for market analysis and trading signals.

## Directory Structure

```
screeners/
├── example_screener/          # Example screener implementation
│   ├── wip/                   # Work-in-progress development
│   ├── final/                 # Final production version
│   └── README.md             # Example screener documentation
└── multi_column/              # Multi-column screeners by information density
    ├── wip/                   # Work-in-progress development
    ├── final/                 # Final production versions
    └── README.md             # Multi-column screener documentation
```

## Development Workflow

### 1. Work in Progress (WIP)
- Develop new screeners in the appropriate `wip/` directory
- Test code in TradingView as you develop
- Use the checkpoint system to track progress

### 2. Production Deployment
- Move finalized logic to `final/` directories
- Ensure all guidelines are followed
- Validate functionality before deployment

## Best Practices

1. **Use Templates**: Start with templates from the `templates/` directory
2. **Follow Guidelines**: Adhere to coding standards in `guidelines/`
3. **Test Thoroughly**: Validate screeners on multiple assets and timeframes
4. **Document Changes**: Keep README files updated with implementation details