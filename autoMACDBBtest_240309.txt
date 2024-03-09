import time
import pyupbit
import pandas as pd

# Set your Upbit API key and secret
# Set your Upbit API key and secret
access = "E8jhhwOAz6xO4sIgBf13L53g06N14OW1gxls9Afv"
secret = "GBZsaNorvShO1uQ9iJiBQ6qQpP8rsOVefbBrRxxZ"
upbit = pyupbit.Upbit(access, secret)

# Set the trading pair and interval
pair = "KRW-BTC"
interval = "minute60"  # You can use "minute1", "minute3", "minute5", "minute15", "minute30", "minute60", "day1"

# Set MACD parameters
fast_length = 12
slow_length = 26
signal_length = 9

# Set Bollinger Bands parameters
bb_length = 20
bb_mult = 2.0

# Set the minimum balance required for trading (10,000 KRW)
min_balance_krw = 10000

while True:
    # Retrieve account balance
    balance_krw = upbit.get_balance(ticker="KRW")
    
    # Proceed with trading only if the account balance is sufficient
    if balance_krw >= min_balance_krw:
        # Retrieve historical candle data
        candles = pyupbit.get_ohlcv(pair, interval, count=max(fast_length, slow_length, signal_length, bb_length))
        
        # Calculate MACD
        exp12 = candles['close'].ewm(span=fast_length, adjust=False).mean()
        exp26 = candles['close'].ewm(span=slow_length, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=signal_length, adjust=False).mean()
        
        # Calculate Bollinger Bands
        basis = candles['close'].rolling(window=bb_length).mean()
        dev = bb_mult * candles['close'].rolling(window=bb_length).std()
        upper_bb = basis + dev
        
        # Get the current close price
        current_close = pyupbit.get_current_price(pair)
        
        # Check for buy and sell signals
        if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-1] <= 0:
            # MACD cross-up (buy) signal with MACD below or equal to 0
            upbit.buy_market_order(pair, 10000) 
            print("MACD Cross-up (Buy) Signal with MACD below or equal to 0")
            # Implement your buy logic here
            # Example: upbit.buy_market_order(pair, 1000000)  # Buy 1,000,000 KRW worth of the asset
        elif current_close < upper_bb.iloc[-1]:
            # Bollinger Bands cross-down (sell) signal
            upbit.sell_market_order(pair, 10000)
            print("Bollinger Bands Cross-down (Sell) Signal")
            # Implement your sell logic here
            # Example: upbit.sell_market_order(pair, 1000000)  # Sell 1,000,000 KRW worth of the asset
    
    # Sleep for a specified interval (e.g., 1 hour)
    time.sleep(10)
