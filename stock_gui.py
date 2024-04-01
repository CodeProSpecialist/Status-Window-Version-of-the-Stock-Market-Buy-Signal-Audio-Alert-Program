import tkinter as tk
import subprocess
import time

def update_display():
    with open('loaded_symbols.txt', 'r') as file:
        symbols = file.read().splitlines()

    # Update text boxes and lights
    for i, symbol in enumerate(symbols):
        symbol_labels[i].config(text=symbol)
        light_indicators[i].config(bg="green" if check_buy_signal(symbol) else "red")

    # Schedule the next update after 2 seconds
    root.after(500, update_display)

def clear_stock_symbols():
    with open('loaded_symbols.txt', 'w') as file:
        file.write('')
    #update_display()

def load_stock_symbols():
    symbols = [entry.get() for entry in entry_boxes if entry.get()]
    with open('loaded_symbols.txt', 'w') as file:
        file.write('\n'.join(symbols))
    update_display()

def check_buy_signal(symbol):
    with open('buy_signals.txt', 'r') as file:
        buy_signals = file.read().splitlines()
    return symbol in buy_signals

def start_scanning():
    # Start the initial update loop
    update_display()
    subprocess.Popen(["gnome-terminal", "--", "python3", "stock_scanner.py"])


def stop_scanning():
    subprocess.run(["pkill", "-f", "stock_scanner.py"])

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Stock Market Buy Signal Audio Alert Program by CodeProSpecialist")
root.attributes('-fullscreen', False)
root.geometry('825x850')

# Create a frame to hold the stock symbol entry boxes
frame = tk.Frame(root)
frame.pack(side=tk.LEFT, fill=tk.Y)

# Create entry boxes for stock symbols
entry_boxes = []
for i in range(25):
    entry = tk.Entry(frame, width=20)
    entry.pack(side=tk.TOP, padx=10, pady=5)
    entry_boxes.append(entry)

# Create a canvas to hold the stock symbol labels and light indicators
canvas = tk.Canvas(root)
canvas.pack(side=tk.RIGHT, fill=tk.Y)

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
    label = tk.Label(frame_on_canvas, text="", width=5, anchor="w")
    label.grid(row=i, column=0, padx=(25, 2), pady=5)  # Adjusted padx to (2, 2)
    symbol_labels.append(label)

    # Create light indicator
    light = tk.Label(frame_on_canvas, width=3, bg="red", anchor="w")
    light.grid(row=i, column=1, padx=(2, 10), pady=5)  # Adjusted padx to (2, 10)
    light_indicators.append(light)

# Create buttons
clear_button = tk.Button(root, text="Clear loaded_symbols.txt ", command=clear_stock_symbols)
clear_button.pack(side=tk.BOTTOM, padx=10, pady=10)

load_button = tk.Button(root, text="Add Stock Symbols to Scanner", command=load_stock_symbols)
load_button.pack(side=tk.TOP, padx=10, pady=10)

start_button = tk.Button(root, text="Start Scanning Stocks", command=start_scanning)
start_button.pack(side=tk.TOP, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Scanning", command=stop_scanning)
stop_button.pack(side=tk.TOP, padx=10, pady=10)

exit_button = tk.Button(root, text="Exit Program", command=exit_program)
exit_button.pack(side=tk.BOTTOM, padx=10, pady=10)


root.mainloop()
