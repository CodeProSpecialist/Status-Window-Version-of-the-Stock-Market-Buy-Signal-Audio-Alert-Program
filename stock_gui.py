import tkinter as tk
from tkinter import messagebox
import subprocess  # Import subprocess module for running external scripts

def save_stock_symbols():
    with open('loaded_symbols.txt', 'w') as file:
        for symbol in loaded_symbols:
            file.write(symbol + '\n')

def clear_stock_symbols():
    # Clear loaded symbols list
    loaded_symbols.clear()
    update_display()
    # Clear loaded_symbols.txt file
    with open('loaded_symbols.txt', 'w') as file:
        pass

def load_stock_symbols():
    global loaded_symbols
    loaded_symbols = []
    for entry in entry_boxes:
        symbol = entry.get()
        if symbol:
            loaded_symbols.append(symbol)
    update_display()

def start_scanning():
    subprocess.Popen(["python3", "stock_scanner.py"])  # Run stock_scanner.py as a separate process

def update_display():
    for i, symbol in enumerate(loaded_symbols):
        recommended, _, _, _, _, _, _, _ = analyze_stock(symbol)
        if recommended:
            indicators_canvas.itemconfig(light_indicators[i], fill="green")
        else:
            indicators_canvas.itemconfig(light_indicators[i], fill="red")

root = tk.Tk()
root.title("Stock Market Analyzer")
root.geometry("1024x768")

# Entry boxes for stock symbols
entry_boxes = []
for i in range(2):
    for j in range(75):
        entry = tk.Entry(root, width=15)
        entry.grid(row=i, column=j, padx=5, pady=5, sticky='w')
        entry_boxes.append(entry)

# Load Stock Symbols Button
load_button = tk.Button(root, text="Load Stock Symbols", command=load_stock_symbols)
load_button.grid(row=2, column=0, padx=10, pady=5, sticky='w')

# Start Scanning Button
start_button = tk.Button(root, text="Start Scanning for Stocks to Buy", command=start_scanning)
start_button.grid(row=0, column=75, padx=10, pady=5, sticky='e')

# Light Indicators Canvas
indicators_canvas = tk.Canvas(root, width=20, height=150)
light_indicators = []
for i in range(2):
    for j in range(75):
        light_indicator = indicators_canvas.create_oval(5 + j*30, 5 + i*40, 25 + j*30, 35 + i*40, fill="white")
        light_indicators.append(light_indicator)
indicators_canvas.grid(row=0, column=76, rowspan=2, padx=10, pady=5, sticky='w')

# Clear Stock Symbols Button
clear_button = tk.Button(root, text="Clear Stock Symbols", command=clear_stock_symbols)
clear_button.grid(row=2, column=76, padx=10, pady=5, sticky='e')

root.mainloop()
