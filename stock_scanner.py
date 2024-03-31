def main():
    next_run_time = get_next_run_time()
    
    while True:
        now = datetime.now()
        
        next_run_time = get_next_run_time()
        print(f"Next run time is:", next_run_time)
        
        if now >= next_run_time:
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
                print(f"MACD: {macd}") # also print if not recommended to buy
                
                if recommended:
                    print(f"{symbol} is recommended to buy today.")
                    subprocess.run(["espeak", f"Buy {symbol}."])
                    plot_stock_data(symbol)
                else:
                    print(f"{symbol} is not recommended to buy today.")
                    plot_stock_data(symbol)

            next_run_time = get_next_run_time()
            print(f"Next run time is:", next_run_time)

        time.sleep(30)

if __name__ == "__main__":
    main()
