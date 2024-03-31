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

def stop_scanning():
    subprocess.run(["pkill", "-f", "stock_scanner.py"])  # Kill stock_scanner.py process

def update_display():
    for i, symbol in enumerate(loaded_symbols):
        if symbol in buy_signals:
            indicators_canvas.itemconfig(light_indicators[i], fill="green")
        else:
            indicators_canvas.itemconfig(light_indicators[i], fill="red")
        label_texts[i].set(symbol)

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
light_indicators = []
label_texts = []
for i in range(75):
    entry = tk.Entry(frame, width=15)
    entry.grid(row=i % 25, column=0, padx=(10, 20), pady=5, sticky='w')
    entry_boxes.append(entry)

    # Create light indicators next to entry boxes
    light_indicator = tk.Canvas(frame, width=20, height=20)
    light_indicator.grid(row=i % 25, column=1, padx=(0, 10), pady=5)
    light_indicator.create_oval(5, 5, 15, 15, fill="white")  # Default color is white
    light_indicators.append(light_indicator)

    # Create labels to display stock symbol names
    label_text = tk.StringVar()
    label = tk.Label(frame, textvariable=label_text)
    label.grid(row=i % 25, column=2, padx=(0, 10), pady=5)
    label_texts.append(label_text)

# Load Stock Symbols Button
load_button = tk.Button(frame, text="Load Stock Symbols", command=load_stock_symbols)
load_button.grid(row=25, column=0, padx=(10, 20), pady=5, sticky='w')

# Start Scanning Button
start_button = tk.Button(frame, text="Start Scanning for Stocks to Buy", command=start_scanning)
start_button.grid(row=26, column=0, padx=(10, 20), pady=5, sticky='w')

# Stop Scanning Button
stop_button = tk.Button(frame, text="Stop Stock Scanner", command=stop_scanning)
stop_button.grid(row=27, column=0, padx=(10, 20), pady=5, sticky='w')

# Clear Stock Symbols Button
clear_button = tk.Button(frame, text="Clear Stock Symbols", command=clear_stock_symbols)
clear_button.grid(row=28, column=0, padx=(10, 20), pady=5, sticky='w')

# Read buy signals
with open('buy_signals.txt', 'r') as file:
    buy_signals = file.read().splitlines()

root.mainloop()
