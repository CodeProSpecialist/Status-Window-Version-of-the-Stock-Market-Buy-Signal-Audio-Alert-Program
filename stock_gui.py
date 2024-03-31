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
        if symbol in buy_signals:
            indicators_canvas.itemconfig(light_indicators[i], fill="green")
        else:
            indicators_canvas.itemconfig(light_indicators[i], fill="red")

root = tk.Tk()
root.title("Stock Market Analyzer")

# Create a canvas with scrollbar
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Entry boxes for stock symbols
entry_boxes = []
for i in range(75):
    entry = tk.Entry(frame, width=15)
    entry.grid(row=i % 25, column=i // 25, padx=5, pady=5, sticky='w')
    entry_boxes.append(entry)

# Load Stock Symbols Button
load_button = tk.Button(frame, text="Load Stock Symbols", command=load_stock_symbols)
load_button.grid(row=25, column=0, columnspan=2, padx=10, pady=5)

# Start Scanning Button
start_button = tk.Button(frame, text="Start Scanning for Stocks to Buy", command=start_scanning)
start_button.grid(row=26, column=0, columnspan=2, padx=10, pady=5)

# Light Indicators Canvas
indicators_canvas = tk.Canvas(frame, width=20, height=75)
light_indicators = []
for i in range(75):
    light_indicator = indicators_canvas.create_oval(5, 5 + i*10, 15, 15 + i*10, fill="white")
    light_indicators.append(light_indicator)
indicators_canvas.grid(row=0, column=2, rowspan=25, padx=10, pady=5)

# Clear Stock Symbols Button
clear_button = tk.Button(frame, text="Clear Stock Symbols", command=clear_stock_symbols)
clear_button.grid(row=27, column=0, columnspan=2, padx=10, pady=5)

# Read buy signals
with open('buy_signals.txt', 'r') as file:
    buy_signals = file.read().splitlines()

root.mainloop()
