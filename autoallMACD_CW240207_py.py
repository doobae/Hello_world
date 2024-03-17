import time
import pyupbit
import pandas as pd

# Set your Upbit API key and secret
access = "ix5Xex6TKVLDJXjbGP3hQUch8JbNxWz0q1zmQkA2"
secret = "PkxbzEu7VIcm3KxyAH56wb2A49dzNIxPg6bLjPNh"
upbit = pyupbit.Upbit(access, secret)

# Set the trading interval
interval = "day"  # You can use "minute1", "minute3", "minute5", "minute15", "minute30", "minute60", "day1"

# Set MACD parameters
fast_length = 12
slow_length = 26
signal_length = 9

# Set the minimum balance required for trading (10,000 KRW)
min_balance_krw = 100000

# Get the list of all trading pairs on Upbit
all_pairs = pyupbit.get_tickers(fiat="KRW")

# Log in
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    for pair in all_pairs:
        try:
            # Retrieve account balance
            balance_krw = upbit.get_balance(ticker="KRW")

            # Proceed with trading only if the account balance is sufficient
            if balance_krw >= min_balance_krw:
                # Retrieve historical candle data
                candles = pyupbit.get_ohlcv(pair, interval, count=max(fast_length, slow_length, signal_length))

                # Calculate MACD
                exp12 = candles['close'].ewm(span=fast_length, adjust=False).mean()
                exp26 = candles['close'].ewm(span=slow_length, adjust=False).mean()
                macd = exp12 - exp26
                signal = macd.ewm(span=signal_length, adjust=False).mean()

                # Get the current close price
                current_close = pyupbit.get_current_price(pair)

                # Check for buy and sell signals
                if macd.iloc[-2] <= signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
                    # MACD cross-up (buy) signal
                    upbit.buy_market_order(pair, 100000)
                    print(f"{pair}: MACD Cross-up (Buy) Signal")
                    # Implement your buy logic here
                    # Example: upbit.buy_market_order(pair, 1000000)  # Buy 1,000,000 KRW worth of the asset
                elif macd.iloc[-2] >= signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
                    # MACD cross-down (sell) signal
                    upbit.sell_market_order(pair, 100000)
                    print(f"{pair}: MACD Cross-down (Sell) Signal")
                    # Implement your sell logic here
                    # Example: upbit.sell_market_order(pair, 1000000)  # Sell 1,000,000 KRW worth of the asset

        except Exception as e:
            # Log the error and continue to the next iteration
            print(f"Error occurred: {str(e)}")
        
        # Sleep for a specified interval (e.g., 10 seconds)
        time.sleep(5)
