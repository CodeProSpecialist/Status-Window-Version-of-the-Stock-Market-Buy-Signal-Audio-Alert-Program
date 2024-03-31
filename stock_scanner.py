import subprocess
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from talib import RSI, MACD
import time
import pytz
import plotext as plt

def get_price_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def calculate_indicators(close_prices):
    rsi = RSI(close_prices, timeperiod=14)
    macd, macd_signal, _ = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    return rsi, macd, macd_signal

def analyze_stock(symbol):
    end_date = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
    start_date_3_months_ago = (datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=90)).strftime('%Y-%m-%d')

    price_data = get_price_data(symbol, start_date_3_months_ago, end_date)

    if price_data.empty:
        print(f"No price data available for {symbol}")
        return False, 0, 0, 0, 0, 0, 0, 0

    close_prices = price_data['Close'].values
    average_volume = np.mean(price_data['Volume'].values)

    current_close_price = close_prices[-1]
    current_open_price = price_data['Open'].iloc[-1]
    current_price = price_data['Close'].iloc[-1]  # Get today's current price
    current_volume = price_data['Volume'].iloc[-1]  # Get today's current volume
    rsi, macd, macd_signal = calculate_indicators(close_prices)

    print(f"\nAnalysis for {symbol}:")
    print(f"Yesterday's Close Price: {current_close_price:.2f}")
    print(f"Open Price for Today: {current_open_price:.2f}")
    print(f"Current Price: {current_price:.2f}")  # Print today's current price
    print(f"Current Volume: {current_volume:.2f}")
    print(f"Average Volume: {average_volume:.2f}")
    print(f"RSI: {rsi}")
    print(f"MACD: {macd}")

    if (rsi[-1] > 58) and \
            (current_volume >= 0.25 * average_volume) and \
            (current_price > current_open_price) and \
            (current_price > current_close_price):
        with open('buy_signals.txt', 'a') as file:
            file.write(f"{symbol}\n")
        return True, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)
    else:
        return False, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)


def plot_stock_data(symbol):
    try:
        end = datetime.now(pytz.timezone('US/Eastern'))
        end = end - timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
        start = end - timedelta(days=365)
        data = get_price_data(symbol, start, end)

        plt.clear()
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.plot(data.index, data['Open'], label='Open Price')
        plt.title(f"{symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"An error occurred while plotting {symbol} data: {e}")

def get_next_run_time():
    now = datetime.now(pytz.timezone('US/Eastern'))

    if now.hour < 10 or (now.hour == 10 and now.minute < 15):
        next_run_time = now.replace(hour=10, minute=15, second=0, microsecond=0)
    elif now.hour < 16:
        next_run_time = now + timedelta(seconds=30)
    else:
        next_run_time = now.replace(hour=10, minute=15, second=0, microsecond=0)
        next_run_time += timedelta(days=1)

    return next_run_time

def main():
    next_run_time = get_next_run_time()
    
    while True:
        now = datetime.now(pytz.timezone('US/Eastern'))
        
        next_run_time = get_next_run_time()
        print(f"Next run time is:", next_run_time.astimezone(pytz.timezone('US/Eastern')))
        
        #if 1 == 1:     #debug code line to run main loop 24 hours
        if now >= next_run_time:
            with open('buy_signals.txt', 'w') as file:
                file.write('')  # Clear contents of buy_signals.txt
            
            with open('loaded_symbols.txt', 'r') as file:
                symbols = file.read().splitlines()

            for symbol in symbols:
                recommended, _, _, _, _, _, _, _ = analyze_stock(symbol)
                if recommended:
                    print(f"{symbol} is recommended to buy today.")
                    subprocess.run(["espeak", f"Buy {symbol}."])
                    plot_stock_data(symbol)

            next_run_time = get_next_run_time()
            print(f"Next run time is:", next_run_time.astimezone(pytz.timezone('US/Eastern')))

        time.sleep(30)

if __name__ == "__main__":
    main()
