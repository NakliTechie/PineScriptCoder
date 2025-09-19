#!/usr/bin/env python3
"""
Generic parameterized script to generate multi-instance PineScript screeners

Usage:
python3 generate_generic_screener.py <market> <num_instances> <tickers_per_instance> <screener_name> <screener_title> <signal_template>

Example:
python3 generate_generic_screener.py us 10 30 BALM "BalM Screener" balm_signal
"""

import os
import sys

def get_market_padding_tickers(market):
    """
    Get market-specific padding tickers for positions beyond active tickers
    
    Args:
        market (str): Market name (e.g., 'us', 'india')
    
    Returns:
        list: List of padding tickers for the market
    """
    if market.lower() == 'us':
        # Crypto tickers for US market
        return ['FILUSDT', 'HOTUSDT', 'SXPUSDT', 'BATS:CSCO', 'RVNUSDT', 
                'ATOMUSDT', 'XRPBNB', 'LTCBTC', 'IOSTBTC', 'GRTUSDT']
    elif market.lower() == 'india':
        # Commodity and crypto tickers for India market
        india_commodities = []
        ticker_file = f'/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt'
        
        if os.path.exists(ticker_file):
            with open(ticker_file, 'r') as f:
                tickers = [line.strip() for line in f.readlines()]
            
            # Look for commodity-related tickers in India market
            commodity_keywords = ['OIL', 'GOLD', 'SILVER', 'STEEL', 'ALUM', 'METAL', 'MINING', 'COPPER']
            for ticker in tickers:
                if any(keyword in ticker.upper() for keyword in commodity_keywords):
                    india_commodities.append(ticker)
                    if len(india_commodities) >= 10:
                        break
        
        # Fill remaining positions with standard crypto tickers
        crypto_tickers = ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD', 'XRPUSD', 
                         'ADAUSD', 'DOGEUSD', 'DOTUSD', 'AVAXUSD', 'LINKUSD']
        
        # Combine commodity tickers (from India market if available) with crypto tickers
        padding_tickers = india_commodities[:10] if india_commodities else []
        
        # Fill remaining positions with crypto tickers
        while len(padding_tickers) < 10:
            padding_tickers.append(crypto_tickers[len(padding_tickers) - len(india_commodities) 
                                if len(padding_tickers) - len(india_commodities) < len(crypto_tickers) 
                                else len(crypto_tickers) - 1])
        
        return padding_tickers
    else:
        # Default crypto tickers for other markets
        return ['FILUSDT', 'HOTUSDT', 'SXPUSDT', 'BATS:CSCO', 'RVNUSDT', 
                'ATOMUSDT', 'XRPBNB', 'LTCBTC', 'IOSTBTC', 'GRTUSDT']

def get_global_commodity_tickers():
    """
    Get global commodity tickers that are commonly available in TradingView
    
    Returns:
        list: List of global commodity, currency, and crypto tickers available in TradingView
    """
    return [
        'CL1!',     # Crude Oil Futures
        'GC1!',     # Gold Futures
        'SI1!',     # Silver Futures
        'HG1!',     # Copper Futures
        'NG1!',     # Natural Gas Futures
        'BTCUSD',   # Bitcoin
        'ETHUSD',   # Ethereum
        'EURUSD',   # Euro/USD
        'GBPUSD',   # British Pound/USD
        'USDJPY',   # USD/Japanese Yen
        'USDCAD',   # USD/Canadian Dollar
        'AUDUSD',   # Australian Dollar/USD
        'NZDUSD',   # New Zealand Dollar/USD
        'XAUUSD',   # Gold Spot
        'XAGUSD',   # Silver Spot
        'GLD',      # SPDR Gold Shares (ETF)
        'SLV',      # iShares Silver Trust (ETF)
        'USOIL',    # US Oil Fund (ETF)
        'XPTUSD',   # Platinum Spot
        'XPDUSD'    # Palladium Spot
    ]

def load_signal_template(template_name):
    """
    Load signal calculation template from file
    
    Args:
        template_name (str): Name of the template file (without extension)
    
    Returns:
        str: Content of the signal template
    """
    template_file = f'/Users/chiragpatnaik/Pinescript/templates/signals/{template_name}.pine'
    
    if not os.path.exists(template_file):
        print(f"Error: Signal template not found: {template_file}")
        return None
    
    with open(template_file, 'r') as f:
        return f.read()

def generate_screener_instances(market, num_instances, tickers_per_instance, screener_name, screener_title, signal_template):
    """
    Generate PineScript screener instances for a given market with market-specific padding
    and global commodity fill for incomplete instances
    
    Args:
        market (str): Market name (e.g., 'us', 'india')
        num_instances (int): Number of instances to generate
        tickers_per_instance (int): Number of tickers per instance
        screener_name (str): Name for the screener (e.g., 'BALM')
        screener_title (str): Title for the screener (e.g., 'BalM Screener')
        signal_template (str): Name of the signal template file (without extension)
    """
    
    # Read all tickers for the specified market
    ticker_file = f'/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt'
    
    if not os.path.exists(ticker_file):
        print(f"Error: Ticker file not found: {ticker_file}")
        return False
    
    with open(ticker_file, 'r') as f:
        tickers = [line.strip() for line in f.readlines()]
    
    # Calculate how many complete instances we can make
    complete_instances = len(tickers) // tickers_per_instance
    remaining_tickers = len(tickers) % tickers_per_instance
    
    print(f"Found {len(tickers)} tickers. Can make {complete_instances} complete instances with {remaining_tickers} remaining tickers.")
    
    # Get market-specific padding tickers (fixed 10 positions for padding)
    padding_tickers = get_market_padding_tickers(market)
    print(f"Using padding tickers for {market} market: {padding_tickers}")
    
    # Get global commodity tickers for filling gaps
    global_commodities = get_global_commodity_tickers()
    print(f"Using global commodity tickers for gap filling: {global_commodities[:10]}...")
    
    # Load signal template
    signal_function_content = load_signal_template(signal_template)
    if signal_function_content is None:
        return False
    
    # Extract function name from template (assuming it's the first function defined)
    # This is a simple approach - in practice you might want a more robust parser
    function_name = None
    lines = signal_function_content.split('\n')
    for line in lines:
        if line.strip().endswith('() =>'):
            # Extract function name without the trailing "()"
            function_name = line.split()[0].rstrip('()')
            break
    
    if function_name is None:
        print("Error: Could not extract function name from template")
        return False
    
    print(f"Using signal function: {function_name}")
    
    # Get signal detection logic based on template name
    if 'balm' in signal_template.lower():
        buy_check = 'str.contains(current_signal, "B")'
        sell_check = 'str.contains(current_signal, "S")'
        buy_increment = 'countBuy += 1'
        sell_increment = 'countSell += 1'
        script_identifier = 'BalM'
    elif 'kurutoga' in signal_template.lower():
        buy_check = 'str.contains(current_signal, "BUY")'
        sell_check = 'str.contains(current_signal, "SELL")'
        buy_increment = 'countBuy += 1'
        sell_increment = 'countSell += 1'
        script_identifier = 'KURU'
    else:
        # Default detection
        buy_check = 'str.contains(current_signal, "BUY")'
        sell_check = 'str.contains(current_signal, "SELL")'
        buy_increment = 'countBuy += 1'
        sell_increment = 'countSell += 1'
        script_identifier = screener_name.upper()
    
    # Create output directory with market subdirectory
    output_dir = f'/Users/chiragpatnaik/Pinescript/screeners/single_column/final/{market}'
    os.makedirs(output_dir, exist_ok=True)
    
    # Total positions in screener (active tickers + padding tickers)
    total_positions = tickers_per_instance + 10  # 30 active + 10 padding
    
    # Generate instances
    for i in range(num_instances):
        instance_num = i + 1
        
        # Get tickers for this instance
        if i < complete_instances:  # Complete instances
            start_idx = i * tickers_per_instance
            end_idx = start_idx + tickers_per_instance
            instance_tickers = tickers[start_idx:end_idx]
        elif i == complete_instances and remaining_tickers > 0:  # Partial instance (use global commodities to fill gaps)
            start_idx = i * tickers_per_instance
            end_idx = start_idx + remaining_tickers
            instance_tickers = tickers[start_idx:end_idx]
            # Fill remaining positions with global commodity tickers instead of duplicating
            global_commodity_idx = 0
            while len(instance_tickers) < tickers_per_instance:
                instance_tickers.append(global_commodities[global_commodity_idx % len(global_commodities)])
                global_commodity_idx += 1
        else:  # Duplicate the last complete instance or partial instance
            if remaining_tickers > 0:
                # Duplicate the partial instance (which already has global commodities filling gaps)
                start_idx = complete_instances * tickers_per_instance
                end_idx = start_idx + remaining_tickers
                instance_tickers = tickers[start_idx:end_idx]
                # Fill remaining positions with global commodity tickers
                global_commodity_idx = 0
                while len(instance_tickers) < tickers_per_instance:
                    instance_tickers.append(global_commodities[global_commodity_idx % len(global_commodities)])
                    global_commodity_idx += 1
            else:
                # Duplicate the last complete instance
                start_idx = (complete_instances - 1) * tickers_per_instance
                end_idx = start_idx + tickers_per_instance
                instance_tickers = tickers[start_idx:end_idx]
        
        # Generate enable flags (total_positions total, first tickers_per_instance enabled, rest disabled)
        enable_flags = []
        for j in range(1, total_positions + 1):
            # First tickers_per_instance tickers enabled, rest disabled
            enabled = j <= tickers_per_instance
            enable_flags.append(f'u{j:02d} = input.bool({str(enabled).lower()}, title = "", group = "Symbols", inline = "s{j:02d}")')
        
        # Generate ticker inputs (total_positions total, first tickers_per_instance from market or global commodities, rest padding)
        ticker_inputs = []
        for j in range(1, total_positions + 1):
            if j <= tickers_per_instance:
                # Market tickers or global commodities
                ticker = instance_tickers[j-1]
                ticker_inputs.append(f's{j:02d} = input.symbol("{ticker}", group = "Symbols", inline = "s{j:02d}")')
            else:
                # Padding tickers
                padding_idx = (j - tickers_per_instance - 1) % len(padding_tickers)
                ticker_inputs.append(f's{j:02d} = input.symbol("{padding_tickers[padding_idx]}", group = "Symbols", inline = "s{j:02d}")')
        
        # Generate security calls
        security_calls = []
        for j in range(1, total_positions + 1):
            security_calls.append(f'signal{j:02d} = request.security(s{j:02d}, timeframe.period, s_expr, lookahead = barmerge.lookahead_off)')
        
        # Generate array sets for barstate.isfirst (fixing indentation issue)
        array_sets = []
        for j in range(total_positions):
            idx = j + 1
            if idx <= tickers_per_instance:
                # Market tickers or global commodities
                array_sets.append(f'    array.set(s_arr, {j}, _only_symbol_name(s{idx:02d}))')
                array_sets.append(f'    array.set(u_arr, {j}, u{idx:02d})')
            else:
                # Padding tickers
                padding_idx = (j - tickers_per_instance) % len(padding_tickers)
                # Extract symbol name (simplified)
                symbol_name = padding_tickers[padding_idx].split(':')[-1].replace('_', '-')
                array_sets.append(f'    array.set(s_arr, {j}, "{symbol_name}")')
                array_sets.append(f'    array.set(u_arr, {j}, u{idx:02d})')
        
        # Generate signal array sets
        signal_array_sets = []
        for j in range(1, total_positions + 1):
            signal_array_sets.append(f'array.set(signal_arr, {j-1}, signal{j:02d})')
        
        # Create the file content - using string replacement instead of format to avoid issues
        file_content = f'''//@version=5
indicator('{script_identifier} - INSTANCE_NUM', overlay = true, max_lines_count = 500, max_labels_count = 500, max_boxes_count = 500)

// --- Inputs ---
// Screener Display
col_width = input.float(5, title = 'Column Width (%)', group = "Screener Display")
scr_numb = input.int(INSTANCE_NUM, title = 'Screen #', tooltip = '1 - rightmost screener', minval = 1, group = "Screener Display")

// Signal Parameters
// (Specific parameters would be defined in the signal template)

//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
// SYMBOLS - Enable Flags
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
ENABLE_FLAGS_PLACEHOLDER

//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
// SYMBOLS - Tickers
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
TICKER_INPUTS_PLACEHOLDER

// --- Script Name ---
string SCRIPT_NAME = "{script_identifier}" 

// --- Colors Definition ---
colorNeutralBG = color.new(color.gray, 0)
colorSignalTXT = color.new(color.white, 0)
colorBuyBG = color.new(color.green, 75)
colorSellBG = color.new(color.red, 75)

// --- Helper function for symbol name ---
_only_symbol_name(s) => 
    string _sym = ""
    if not na(s)
        if str.contains(s, ":")
            _sym := array.get(str.split(s, ':'), 1)
        else
            _sym := s
        _sym := str.replace_all(_sym, "_", "-")
    _sym

// --- Helper function to calculate midpoint ---
_calc_midpoint(h, l) =>
    (h + l) / 2

// --- Signal Calculation Function (Loaded from template) ---
{signal_function_content}

// --- Security Calls ---
s_expr = {function_name}() 

SECURITY_CALLS_PLACEHOLDER

// --- ARRAYS ---
var s_arr = array.new_string({total_positions})
var u_arr = array.new_bool({total_positions})
var signal_arr = array.new_string({total_positions})

if barstate.isfirst
ARRAY_SETS_PLACEHOLDER

// Update signal_arr on every bar
SIGNAL_ARRAY_SETS_PLACEHOLDER


// --- Table Drawing ---
var tbl = table.new(position.top_right, scr_numb > 1 ? 3 : 2, 50, frame_color = #151715, frame_width = 1, border_width = 2, border_color = color.new(color.white, 100))

if barstate.islast
    table.clear(tbl, 0, 0, scr_numb > 1 ? 2 : 1, 49)

    var int countBuy = 0
    var int countSell = 0
    countBuy := 0
    countSell := 0

    int rounded_col_width = int(math.round(col_width))

    string header_text = SCRIPT_NAME + " - " + str.tostring(scr_numb)
    table.cell(tbl, 0, 0, 'Symbol', width = rounded_col_width, text_halign = text.align_center, bgcolor = color.gray, text_color = color.white, text_size = size.small)
    table.cell(tbl, 1, 0, header_text, width = rounded_col_width, text_halign = text.align_center, bgcolor = color.gray, text_color = color.white, text_size = size.small)
    if scr_numb > 1
        table.cell(tbl, 2, 0, '', width = rounded_col_width * 2 * (scr_numb - 1), text_halign = text.align_center, bgcolor = color.new(color.gray, 100), text_size = size.small)

    int visible_row_index = 1 
    for i = 0 to {total_positions - 1} by 1
        if array.get(u_arr, i) 
            string signal_val_from_array = array.get(signal_arr, i)
            string current_signal = na(signal_val_from_array) ? "---" : signal_val_from_array
            string ticker_name = array.get(s_arr, i)

            color signal_bg_col = colorNeutralBG 
            
            if {buy_check}
                {buy_increment}
                signal_bg_col := colorBuyBG
            else if {sell_check}
                {sell_increment}
                signal_bg_col := colorSellBG

            table.cell(tbl, 0, visible_row_index, ticker_name, text_halign = text.align_center, bgcolor = color.gray, text_color = color.white, text_size = size.small, width = rounded_col_width)
            table.cell(tbl, 1, visible_row_index, current_signal, text_halign = text.align_center, bgcolor = signal_bg_col, text_color = colorSignalTXT, text_size = size.small, width = rounded_col_width)

            visible_row_index += 1
'''
        
        # Replace placeholders
        file_content = file_content.replace('INSTANCE_NUM', str(instance_num))
        file_content = file_content.replace('ENABLE_FLAGS_PLACEHOLDER', '\n'.join(enable_flags))
        file_content = file_content.replace('TICKER_INPUTS_PLACEHOLDER', '\n'.join(ticker_inputs))
        file_content = file_content.replace('SECURITY_CALLS_PLACEHOLDER', '\n'.join(security_calls))
        file_content = file_content.replace('ARRAY_SETS_PLACEHOLDER', '\n'.join(array_sets))
        file_content = file_content.replace('SIGNAL_ARRAY_SETS_PLACEHOLDER', '\n'.join(signal_array_sets))
        
        # Fix the stray "SIGNAL_" text issue by replacing it with empty string
        file_content = file_content.replace('SIGNAL_', '')
        
        # Write to file
        filename = f'{output_dir}/screener_{screener_name.lower()}_{instance_num}.txt'
        with open(filename, 'w') as f:
            f.write(file_content)
            
        print(f"Created {filename}")
    
    print(f"All {num_instances} instances created successfully for {market} market!")
    return True

def main():
    if len(sys.argv) != 7:
        print("Usage: python3 generate_generic_screener.py <market> <num_instances> <tickers_per_instance> <screener_name> <screener_title> <signal_template>")
        print('Example: python3 generate_generic_screener.py us 10 30 BALM "BalM Screener" balm_signal')
        sys.exit(1)
    
    market = sys.argv[1]
    num_instances = int(sys.argv[2])
    tickers_per_instance = int(sys.argv[3])
    screener_name = sys.argv[4]
    screener_title = sys.argv[5]
    signal_template = sys.argv[6]
    
    success = generate_screener_instances(market, num_instances, tickers_per_instance, screener_name, screener_title, signal_template)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()