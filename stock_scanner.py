# stock_scanner.py

import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from talib import RSI, MACD
import pytz
import time
from stock_common import load_stock_symbols  # Import load_stock_symbols function from stock_common module

def get_price_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def calculate_indicators(data):
    close_prices = data[:, 4]
    rsi = RSI(close_prices, timeperiod=14)
    macd, macd_signal, _ = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    return rsi, macd, macd_signal

def analyze_stock(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date_3_months_ago = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

    price_data = get_price_data(symbol, start_date_3_months_ago, end_date).values

    current_close_price = price_data[-1, 3]
    current_open_price = get_opening_price(symbol)
    current_price = get_current_price(symbol)  # Get today's current price
    current_volume = price_data[-1, 5]
    average_volume = np.mean(price_data[:, 5])

    rsi, macd, macd_signal = calculate_indicators(price_data)

    if (rsi[-1] > 58) and \
            (current_volume >= 0.25 * average_volume) and \
            (current_price > current_open_price) and \
            (current_price > current_close_price):
        with open('buy_signals.txt', 'a') as file:
            file.write(symbol + '\n')  # Write symbol to buy_signals.txt
        return True
    else:
        return False

def get_opening_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)

def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period='1d')['Close'].iloc[0], 4)

def main():
    next_run_time = datetime.now() + timedelta(seconds=30)
    
    symbols = load_stock_symbols()  # Load stock symbols
    
    while True:
        now = datetime.now()
        
        if now >= next_run_time:
            with open('buy_signals.txt', 'w') as file:
                file.write('')  # Clear contents of buy_signals.txt
            
            print("Recommended Stocks to Buy Today:")
            
            for symbol in symbols:
                if analyze_stock(symbol):
                    print(f"{symbol} is recommended to buy today.")
                else:
                    print(f"{symbol} is not recommended to buy today.")

            next_run_time = datetime.now() + timedelta(seconds=30)

        time.sleep(1)

if __name__ == "__main__":
    main()
