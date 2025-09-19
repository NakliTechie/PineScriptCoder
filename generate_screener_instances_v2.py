#!/usr/bin/env python3
"""
Parameterized script to generate multi-instance PineScript screeners with market-specific padding strategies
and global commodity fill for incomplete instances

Usage:
python3 generate_screener_instances_v2.py <market> <num_instances> <base_script_name> <script_title> <screener_type>

Example:
python3 generate_screener_instances_v2.py us 10 BALM "BalM Screener" balm
python3 generate_screener_instances_v2.py us 10 KURU "Kurutoga Screener" kurutoga
"""

import os
import sys

def get_market_padding_tickers(market):
    """
    Get market-specific padding tickers for positions 31-40
    
    Args:
        market (str): Market name (e.g., 'us', 'india')
    
    Returns:
        list: List of 10 padding tickers for the market
    """
    if market.lower() == 'us':
        # Crypto tickers for US market
        return ['FILUSDT', 'HOTUSDT', 'SXPUSDT', 'BATS:CSCO', 'RVNUSDT', 
                'ATOMUSDT', 'XRPBNB', 'LTCBTC', 'IOSTBTC', 'GRTUSDT']
    elif market.lower() == 'india':
        # Commodity and crypto tickers for India market
        # First try to use commodity stocks from India market
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
    Get global commodity tickers to fill gaps in incomplete instances
    Using tickers that are commonly available in TradingView
    
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
        'USOIL',    # US Oil Fund (ETF)
        'GLD',      # SPDR Gold Shares (ETF)
        'SLV',      # iShares Silver Trust (ETF)
        'XPTUSD',   # Platinum Spot
        'XPDUSD'    # Palladium Spot
    ]

def get_signal_function(screener_type):
    """
    Get the signal calculation function based on screener type
    
    Args:
        screener_type (str): Type of screener ('kurutoga' or 'balm')
    
    Returns:
        str: Pine Script function code
    """
    if screener_type.lower() == 'kurutoga':
        return '''// --- Calculation Function for request.security ---
calculateKurutogaSignal() => 
    // Define the three lengths
    len1 = baseLength
    len2 = baseLength * 2
    len3 = baseLength * 4

    // Calculations for Length 1 (baseLength)
    high1 = ta.highest(high, len1)
    low1 = ta.lowest(low, len1)
    midpoint1 = _calc_midpoint(high1, low1)
    divergence1 = close - midpoint1

    // Calculations for Length 2 (2 * baseLength)
    high2 = ta.highest(high, len2)
    low2 = ta.lowest(low, len2)
    midpoint2 = _calc_midpoint(high2, low2)
    divergence2 = close - midpoint2

    // Calculations for Length 3 (4 * baseLength)
    high3 = ta.highest(high, len3)
    low3 = ta.lowest(low, len3)
    midpoint3 = _calc_midpoint(high3, low3)
    divergence3 = close - midpoint3

    // Signal Logic
    // Bullish condition: All three are positive, and weren't on the previous bar
    allPositive = divergence1 > 0 and divergence2 > 0 and divergence3 > 0
    bullishSignal = allPositive and not allPositive[1]

    // Bearish condition: All three are negative, and weren't on the previous bar
    allNegative = divergence1 < 0 and divergence2 < 0 and divergence3 < 0
    bearishSignal = allNegative and not allNegative[1]

    // Signal Determination
    string signalCode = "---"
    if bullishSignal
        signalCode := "BUY"
    else if bearishSignal
        signalCode := "SELL"

    // Append percentage change if a signal exists
    if signalCode != "---"
        // Use the current bar's close and previous bar's close for percentage change
        float pct_change = ((close - close[1]) / close[1]) * 100.0
        string pct_change_str = str.format("{0,number,#.##}%", pct_change)
        signalCode := signalCode + " " + pct_change_str
        
    signalCode'''
    elif screener_type.lower() == 'balm':
        return '''// --- Calculation Function for request.security ---
calculateBalMSignal() => 
    // EMA calculations (simplified for screener)
    EMAHigh = ta.ema(high, 4)
    EMALow = ta.ema(low, 4)
    
    // Base Ballista signals (only these two as requested)
    ballista_buy = close > EMAHigh and close[1] < EMAHigh[1] and close[2] < EMAHigh[2] and close[3] < EMAHigh[3]
    ballista_sell = close < EMALow and close[1] > EMALow[1] and close[2] > EMALow[2] and close[3] > EMALow[3]
    
    // Signal Determination - Simplified to only use base signals with B/S labels
    string signalCode = "---"
    if ballista_buy
        signalCode := "B"
    else if ballista_sell
        signalCode := "S"
    
    // Append percentage change if a signal exists
    if signalCode != "---"
        float pct_change = ((close - close[1]) / close[1]) * 100.0
        string pct_change_str = str.format("{0,number,#.##}%", pct_change)
        signalCode := signalCode + " " + pct_change_str
        
    signalCode'''
    else:
        raise ValueError(f"Unsupported screener type: {screener_type}")

def get_function_name(screener_type):
    """
    Get the function name based on screener type
    
    Args:
        screener_type (str): Type of screener ('kurutoga' or 'balm')
    
    Returns:
        str: Function name
    """
    if screener_type.lower() == 'kurutoga':
        return 'calculateKurutogaSignal'
    elif screener_type.lower() == 'balm':
        return 'calculateBalMSignal'
    else:
        raise ValueError(f"Unsupported screener type: {screener_type}")

def get_script_name(screener_type):
    """
    Get the script name based on screener type
    
    Args:
        screener_type (str): Type of screener ('kurutoga' or 'balm')
    
    Returns:
        str: Script name
    """
    if screener_type.lower() == 'kurutoga':
        return 'KURU'
    elif screener_type.lower() == 'balm':
        return 'BalM'
    else:
        raise ValueError(f"Unsupported screener type: {screener_type}")

def get_signal_detection_logic(screener_type):
    """
    Get the signal detection logic for the table drawing section
    
    Args:
        screener_type (str): Type of screener ('kurutoga' or 'balm')
    
    Returns:
        tuple: (buy_signal_check, sell_signal_check, buy_count_increment, sell_count_increment)
    """
    if screener_type.lower() == 'kurutoga':
        return (
            'str.contains(current_signal, "BUY")',
            'str.contains(current_signal, "SELL")',
            'countBuy += 1',
            'countSell += 1'
        )
    elif screener_type.lower() == 'balm':
        return (
            'str.contains(current_signal, "B")',
            'str.contains(current_signal, "S")',
            'countBuy += 1',
            'countSell += 1'
        )
    else:
        raise ValueError(f"Unsupported screener type: {screener_type}")

def generate_screener_instances(market, num_instances, base_script_name, script_title, screener_type):
    """
    Generate PineScript screener instances for a given market with market-specific padding
    and global commodity fill for incomplete instances
    
    Args:
        market (str): Market name (e.g., 'us', 'india')
        num_instances (int): Number of instances to generate
        base_script_name (str): Base name for the script (e.g., 'BALM')
        script_title (str): Title for the script (e.g., 'BalM Screener')
        screener_type (str): Type of screener ('kurutoga' or 'balm')
    """
    
    # Read all tickers for the specified market
    ticker_file = f'/Users/chiragpatnaik/Pinescript/tickers/{market}/all_tickers.txt'
    
    if not os.path.exists(ticker_file):
        print(f"Error: Ticker file not found: {ticker_file}")
        return False
    
    with open(ticker_file, 'r') as f:
        tickers = [line.strip() for line in f.readlines()]
    
    # Calculate how many complete instances we can make
    tickers_per_instance = 30  # Fixed to 30 active tickers per instance
    complete_instances = len(tickers) // tickers_per_instance
    remaining_tickers = len(tickers) % tickers_per_instance
    
    print(f"Found {len(tickers)} tickers. Can make {complete_instances} complete instances with {remaining_tickers} remaining tickers.")
    
    # Get market-specific padding tickers
    padding_tickers = get_market_padding_tickers(market)
    print(f"Using padding tickers for {market} market: {padding_tickers}")
    
    # Get global commodity tickers for filling gaps
    global_commodities = get_global_commodity_tickers()
    print(f"Using global commodity tickers for gap filling: {global_commodities[:10]}...")
    
    # Get signal function based on screener type
    signal_function = get_signal_function(screener_type)
    function_name = get_function_name(screener_type)
    script_name = get_script_name(screener_type)
    
    # Get signal detection logic
    buy_check, sell_check, buy_increment, sell_increment = get_signal_detection_logic(screener_type)
    
    # Create output directory with market subdirectory
    output_dir = f'/Users/chiragpatnaik/Pinescript/screeners/single_column/final/{market}'
    os.makedirs(output_dir, exist_ok=True)
    
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
        
        # Generate enable flags (40 total, first 30 enabled, last 10 disabled)
        enable_flags = []
        for j in range(1, 41):
            # First 30 tickers enabled, last 10 disabled
            enabled = j <= 30
            enable_flags.append(f'u{j:02d} = input.bool({str(enabled).lower()}, title = "", group = "Symbols", inline = "s{j:02d}")')
        
        # Generate ticker inputs (40 total, first 30 from market or global commodities, last 10 padding)
        ticker_inputs = []
        for j in range(1, 41):
            if j <= 30:
                # Market tickers or global commodities
                ticker = instance_tickers[j-1]
                ticker_inputs.append(f's{j:02d} = input.symbol("{ticker}", group = "Symbols", inline = "s{j:02d}")')
            else:
                # Padding tickers (positions 31-40)
                padding_idx = (j - 31) % len(padding_tickers)
                ticker_inputs.append(f's{j:02d} = input.symbol("{padding_tickers[padding_idx]}", group = "Symbols", inline = "s{j:02d}")')
        
        # Generate security calls
        security_calls = []
        for j in range(1, 41):
            security_calls.append(f'signal{j:02d} = request.security(s{j:02d}, timeframe.period, s_expr, lookahead = barmerge.lookahead_off)')
        
        # Generate array sets for barstate.isfirst (fixing indentation issue)
        array_sets = []
        for j in range(40):
            idx = j + 1
            if idx <= 30:
                # Market tickers or global commodities
                array_sets.append(f'    array.set(s_arr, {j}, _only_symbol_name(s{idx:02d}))')
                array_sets.append(f'    array.set(u_arr, {j}, u{idx:02d})')
            else:
                # Padding tickers
                padding_idx = (j - 30) % len(padding_tickers)
                # Extract symbol name (simplified)
                symbol_name = padding_tickers[padding_idx].split(':')[-1].replace('_', '-')
                array_sets.append(f'    array.set(s_arr, {j}, "{symbol_name}")')
                array_sets.append(f'    array.set(u_arr, {j}, u{idx:02d})')
        
        # Generate signal array sets
        signal_array_sets = []
        for j in range(1, 41):
            signal_array_sets.append(f'array.set(signal_arr, {j-1}, signal{j:02d})')
        
        # Prepare signal parameters based on screener type
        signal_params = "" if screener_type.lower() == 'balm' else "baseLength = input.int(14, title=\"Base Length\", minval=1, group=\"Signal Parameters\")"
        
        # Create the file content
        file_content = f'''//@version=5
indicator('{script_name} - {instance_num}', overlay = true, max_lines_count = 500, max_labels_count = 500, max_boxes_count = 500)

// --- Inputs ---
// Screener Display
col_width = input.float(5, title = 'Column Width (%)', group = "Screener Display")
scr_numb = input.int({instance_num}, title = 'Screen #', tooltip = '1 - rightmost screener', minval = 1, group = "Screener Display")

// Signal Parameters
{signal_params}

//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
// SYMBOLS - Enable Flags
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
{'\n'.join(enable_flags)}

//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
// SYMBOLS - Tickers
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
{'\n'.join(ticker_inputs)}

// --- Script Name ---
string SCRIPT_NAME = "{script_name}" 

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

{signal_function}

// --- Security Calls ---
s_expr = {function_name}() 

{'\n'.join(security_calls)}

// --- ARRAYS ---
var s_arr = array.new_string(40)
var u_arr = array.new_bool(40)
var signal_arr = array.new_string(40)

if barstate.isfirst
{'\n'.join(array_sets)}

// Update signal_arr on every bar
{'\n'.join(signal_array_sets)}


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
    for i = 0 to 39 by 1
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

        # Write to file
        filename = f'{output_dir}/screener_{base_script_name.lower()}_{instance_num}.txt'
        with open(filename, 'w') as f:
            f.write(file_content)
            
        print(f"Created {filename}")
    
    print(f"All {num_instances} instances created successfully for {market} market!")
    return True

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 generate_screener_instances_v2.py <market> <num_instances> <base_script_name> <script_title> <screener_type>")
        print('Example: python3 generate_screener_instances_v2.py us 10 BALM "BalM Screener" balm')
        print('Example: python3 generate_screener_instances_v2.py us 10 KURU "Kurutoga Screener" kurutoga')
        sys.exit(1)
    
    market = sys.argv[1]
    num_instances = int(sys.argv[2])
    base_script_name = sys.argv[3]
    script_title = sys.argv[4]
    screener_type = sys.argv[5]
    
    success = generate_screener_instances(market, num_instances, base_script_name, script_title, screener_type)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()