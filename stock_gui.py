import tkinter as tk
import subprocess

entry_boxes = []

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
    for entry in entry_boxes:
        entry.delete(0, tk.END)


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


def close_symbol_entry_window():
    entry_window.destroy()


def open_symbol_entry_window():
    global entry_window  # Declare entry_window as global
    global entry_boxes  # Declare entry_boxes as global

    entry_window = tk.Toplevel(root)
    entry_window.title("Update Stock Symbols List")
    entry_window.geometry('800x700')

    frame = tk.Frame(entry_window)
    frame.pack(side=tk.LEFT, fill=tk.Y)

    canvas = tk.Canvas(entry_window)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(entry_window, orient=tk.VERTICAL, width=15, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame_on_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_on_canvas, anchor="nw")

    add_close_window_button = tk.Button(frame_on_canvas, text="Close Window", width=20, command=close_symbol_entry_window)
    add_close_window_button.pack(side=tk.RIGHT, padx=5, pady=5, anchor="ne")

    # Add "Add Stock Symbols" button
    add_symbols_button = tk.Button(frame_on_canvas, text="Add Stock Symbols", width=20, command=load_stock_symbols)
    add_symbols_button.pack(side=tk.RIGHT, padx=5, pady=5, anchor="ne")

    entry_boxes = []
    for i in range(512):
        entry = tk.Entry(frame_on_canvas, width=20)
        entry.pack(side=tk.TOP, padx=5, pady=2)
        entry_boxes.append(entry)


root = tk.Tk()
root.title("Stock Market Buy Signal Audio Alert Program by CodeProSpecialist")
root.attributes('-fullscreen', False)
root.geometry('1820x1024')

# Create a canvas to hold the stock symbol labels and light indicators
canvas_east = tk.Canvas(root)
canvas_east.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame to hold the light indicators and corresponding labels
frame_on_canvas = tk.Frame(canvas_east)
frame_on_canvas.pack(fill=tk.BOTH, expand=True)

# Create a list to store labels and light indicators
symbol_labels = []
light_indicators = []

# Create 15 columns of 10 labels for stock symbols and light indicators
for i in range(16):
    for j in range(32):
        symbol_label = tk.Label(frame_on_canvas, text="", width=7, anchor="w")
        symbol_label.grid(row=j, column=i * 2, padx=(10, 2), pady=2)
        symbol_labels.append(symbol_label)

        light = tk.Label(frame_on_canvas, width=3, bg="red", anchor="w")
        light.grid(row=j, column=i * 2 + 1, padx=(2, 10), pady=2)
        light_indicators.append(light)

# Create buttons
update_symbols_button = tk.Button(root, text="Update Stock Symbols List", width=30, command=open_symbol_entry_window)
update_symbols_button.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=5)

start_button = tk.Button(root, text="Start Scanning", width=30, command=start_scanning)
start_button.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=5)

stop_button = tk.Button(root, text="Stop Scanning", width=30, command=stop_scanning)
stop_button.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=5)

clear_button = tk.Button(root, text="Clear Symbols", width=30, command=clear_stock_symbols)
clear_button.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=5)

exit_button = tk.Button(root, text="Exit Program", width=30, command=exit_program)
exit_button.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=5)


root.mainloop()
