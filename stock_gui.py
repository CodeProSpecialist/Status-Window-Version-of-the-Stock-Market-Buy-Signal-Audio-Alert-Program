import tkinter as tk
import subprocess

def update_display():
    with open('loaded_symbols.txt', 'r') as file:
        symbols = file.read().splitlines()

    # Update text boxes and lights
    for i, symbol in enumerate(symbols):
        symbol_labels[i].config(text=symbol)
        light_indicators[i].config(bg="green" if check_buy_signal(symbol) else "red")

def clear_stock_symbols():
    with open('loaded_symbols.txt', 'w') as file:
        file.write('')
    update_display()

def load_stock_symbols():
    symbols = [entry.get() for entry in entry_boxes if entry.get()]
    with open('loaded_symbols.txt', 'w') as file:
        file.write('\n'.join(symbols))
    update_display()

def check_buy_signal(symbol):
    with open('buy_signals.txt', 'r') as file:
        buy_signals = file.read().splitlines()
    return symbol in buy_signals

root = tk.Tk()
root.title("Stock GUI")
root.geometry("1024x768")

# Create a frame to hold the stock symbol entry boxes
frame = tk.Frame(root)
frame.pack()

# Create entry boxes for stock symbols
entry_boxes = []
for i in range(25):
    entry = tk.Entry(frame, width=20)
    entry.grid(row=i, column=0, padx=10, pady=5)
    entry_boxes.append(entry)

# Create a canvas to hold the stock symbol labels and light indicators
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.Y)

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame on the canvas to hold the stock symbol labels and light indicators
frame_on_canvas = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_on_canvas, anchor="nw")

# List to store the labels and light indicators
symbol_labels = []
light_indicators = []

# Create 25 labels for stock symbols
for i in range(25):
    label = tk.Label(frame_on_canvas, text="", width=20, anchor="w")
    label.grid(row=i, column=1, padx=10, pady=5)
    symbol_labels.append(label)

    # Create light indicator
    light = tk.Label(frame_on_canvas, width=3, bg="red")
    light.grid(row=i, column=2, padx=10, pady=5)
    light_indicators.append(light)

# Create buttons
clear_button = tk.Button(root, text="Clear Stock Symbols", command=clear_stock_symbols)
clear_button.pack(side=tk.BOTTOM, padx=10, pady=10)

load_button = tk.Button(root, text="Load Stock Symbols", command=load_stock_symbols)
load_button.pack(side=tk.BOTTOM, padx=10, pady=10)

update_display()  # Update display initially
root.mainloop()
