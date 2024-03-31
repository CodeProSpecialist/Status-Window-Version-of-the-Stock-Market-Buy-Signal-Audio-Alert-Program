# stock_scanner.py

import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from talib import RSI, MACD
import pytz
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
        return True
    else:
        return False

def get_opening_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period="1d")["Open"].iloc[0], 4)

def get_current_price(symbol):
    stock_data = yf.Ticker(symbol)
    return round(stock_data.history(period='1d')['Close'].iloc[0], 4)

def get_previous_weekday(date):
    while date.weekday() > 4:  # Monday is 0, Friday is 4
        date -= timedelta(days=1)
    return date

def generate_buy_signals(etfs):
    buy_signals = []
    for etf in etfs:
        if analyze_stock(etf):
            buy_signals.append(etf + '\n')

    with open('buy_signals.txt', 'w') as file:
        file.writelines(buy_signals)

def main():
    eastern = pytz.timezone('US/Eastern')
    next_run_time = get_next_run_time()
    next_run_time2 = datetime.now(eastern)

    print("")
    print("Stock Market Buy Signal Audio Alert Program by CodeProSpecialist ")
    print("")
    print("Date and Time: ", datetime.now(eastern).strftime("%A, %B %d, %Y, %I:%M:%S %p"), "Eastern ")
    print("")
    print("This program runs from 10:15 AM until 4:00 PM, Eastern, Monday - Friday. ")
    print("")
    subprocess.run(["espeak",
                    "Remember to not buy before 10:15 AM and do not buy before I recommend to buy or you are buying based on emotion and emotion or excitement buying is not productive. "])

    subprocess.run(["espeak", "Always wait at least 1 month before buying an IPO or Initial Public Offering or else the price will almost always decrease by 95%.  "])

    print("")
    print("This program will begin in 30 seconds. ")
    subprocess.run(["espeak", "This program will begin in 30 seconds. "])

    print("")
    # print("Next Run Time:", next_run_time.astimezone(eastern).strftime("%A, %B %d, %Y, %I:%M:%S %p"), "Eastern ")
    print("")

    while True:
        now = datetime.now(eastern)

        if now >= next_run_time and now.hour < 16:
        #if 1 == 1:      #debug code line to bypass if statement
            if now.weekday() < 5:
            #if 1 == 1:     #debug code line to bypass if statement
                    print("Recommended Stocks to Buy Today:")
                    etfs = ['VGT', 'VOOV', 'VOT', 'SPMD', 'UMDD', 'VTI', 'VGT']

                    generate_buy_signals(etfs)

                    time.sleep(0.5)

                    next_run_time2 += timedelta(seconds=30)
                    print("\nNext Run Time:", next_run_time2.astimezone(eastern).strftime("%A, %B %d, %Y, %I:%M:%S %p"), "Eastern ")

        time.sleep(30)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("An error occurred:", e)
            print("Restarting the program in 5 seconds.....")
            time.sleep(5)
