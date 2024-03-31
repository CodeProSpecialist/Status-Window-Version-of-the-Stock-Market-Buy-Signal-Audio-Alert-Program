import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from talib import RSI, MACD
import time

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

    if len(price_data) == 0:
        print(f"No price data available for {symbol}")
        return False, 0, 0, 0, 0, 0, 0, 0

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
        return True, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)
    else:
        return False, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)


def get_opening_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)

def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period='1d')['Close'].iloc[0], 4)

def main():
    next_run_time = datetime.now() + timedelta(seconds=30)
    
    while True:
        now = datetime.now()
        
        if now >= next_run_time:
            with open('buy_signals.txt', 'w') as file:
                file.write('')  # Clear contents of buy_signals.txt
            
            with open('loaded_symbols.txt', 'r') as file:
                symbols = file.read().splitlines()

            for symbol in symbols:
                if analyze_stock(symbol):
                    print(f"{symbol} is recommended to buy today.")
                else:
                    print(f"{symbol} is not recommended to buy today.")

            next_run_time = datetime.now() + timedelta(seconds=30)

        time.sleep(1)

if __name__ == "__main__":
    main()
