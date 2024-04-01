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

def calculate_indicators(data):
    close_prices = data[:, 4]
    rsi = RSI(close_prices, timeperiod=14)
    macd, macd_signal, _ = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    return rsi, macd, macd_signal

def get_opening_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)

def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period='1d')['Close'].iloc[0], 4)

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
        return True, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)
    else:
        return False, round(current_close_price, 2), round(current_open_price, 2), round(current_price, 2), current_volume, average_volume, round(rsi[-1], 2), round(macd[-1], 2)

def get_previous_weekday(date):
    while date.weekday() > 4:  # Monday is 0, Friday is 4
        date -= timedelta(days=1)
    return date


def plot_stock_data(symbol):
    try:
        end = get_previous_weekday(datetime.today())
        start = get_previous_weekday(end - timedelta(days=365))
        data = yf.download(symbol, start, end)

        plt.clear_data()

        # Plotting candlesticks manually
        for i, (_, row) in enumerate(data.iterrows()):
            plt.plot([i, i], [row['High'], row['Low']], color='black')
            if row['Open'] < row['Close']:
                plt.plot([i, i], [row['Open'], row['Close']], color='green')
            else:
                plt.plot([i, i], [row['Open'], row['Close']], color='red')

        plt.title(f"{symbol} Stock Price")
        plt.xlabel("Date")
        plt.ylabel("Price")

        # Customize x-axis ticks to show day/month/year format with month in all capital letters and extra space between components
        x_ticks = [date.strftime("%d-%b-%Y").upper() for date in data.index]
        plt.xticks(ticks=range(len(x_ticks)), labels=x_ticks)

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
        
        if 1 == 1:     #debug code line to run main loop 24 hours
        #if now >= next_run_time:
            with open('buy_signals.txt', 'w') as file:
                file.write('')  # Clear contents of buy_signals.txt
            
            with open('loaded_symbols.txt', 'r') as file:
                symbols = file.read().splitlines()

            for symbol in symbols:
                recommended, close_price, open_price, current_price, current_volume, average_volume, rsi, macd = analyze_stock(symbol)

                print(f"\nAnalysis for {symbol}:")
                print(f"Yesterday's Close Price: {close_price:.2f}")
                print(f"Open Price for Today: {open_price:.2f}")
                print(f"Current Price: {current_price:.2f}")  # Print today's current price
                print(f"Current Volume: {current_volume:.2f}")
                print(f"Average Volume: {average_volume:.2f}")
                print(f"RSI: {rsi}")
                print(f"MACD: {macd}")

                plot_stock_data(symbol)

                recommended, _, _, _, _, _, _, _ = analyze_stock(symbol)
                if recommended:
                    print(f"{symbol} is recommended to buy today.")
                    subprocess.run(["espeak", f"Buy {symbol}."])
                    with open('buy_signals.txt', 'a') as file:
                        file.write(f"{symbol}\n")

            next_run_time = get_next_run_time()
            print(f"Next run time is:", next_run_time.astimezone(pytz.timezone('US/Eastern')))

        time.sleep(30)

if __name__ == "__main__":
    main()
