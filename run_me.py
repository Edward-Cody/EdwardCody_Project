"""Summary: This file mostly handles the GUI while app.py handles the majority of the processing. Details: This file creates the GUI, starts and stops the Flask server, records the first URL, takes the first web page screenshot, records the time spent on the last web page, and opens results.html in the browser."""

import matplotlib.pyplot as plt
import os
import pandas as pd
import pyautogui
import requests
import seaborn as sns
import subprocess
import threading
import time
import tkinter as tk
import webbrowser

from flask import jsonify
from tkinter import font, messagebox
from screeninfo import get_monitors


# Get screen dimensions
screen = get_monitors()[0]  # Assumes a single monitor setup; otherwise specify the desired monitor
screen_width = screen.width
screen_height = screen.height
screen_width_str = str(screen_width)
screen_height_str = str(screen_height)

# Function to start the Flask server in a separate thread
def start_flask_server():
    global flask_process
    flask_process = subprocess.Popen(["python", "app.py"])
    print("Flask server started.")

# Function to send the URL to the Flask app, open it, and log it in CSV
def start_recording():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    try:
        # Record the URL in URL_clicks.csv
        csv_filepath = "data/URL_clicks.csv"
        current_timestamp = time.time()
        with open(csv_filepath, "a+") as f:
            f.write(f"{current_timestamp}, {url}, \n")  # Append the URL with timestamp and blank time spent

        # Send the URL to the Flask app and open it in the browser
        response = requests.get(f"http://127.0.0.1:3000/start", params={"url": url})
        if response.ok:
            webbrowser.open(url)  # Open the URL in the default browser
        else:
            messagebox.showerror("Error", f"Failed to start recording. Server response: {response.status_code}")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Could not connect to the server. Is the Flask app running?")
    
    try:
        time.sleep(1)  # Wait for the page to load
        screenshot = pyautogui.screenshot()
        screenshot_path = f'static/data/screenshot_page1.png'
        screenshot.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}.")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return jsonify(status='error', message="Failed to take screenshot"), 500
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open the "show_results.html" file
def stop_recording():
    global previous_timestamp

    # Calculate and record time spent for the last row in URL_clicks.csv
    csv_filepath = "data/URL_clicks.csv"
    current_timestamp = time.time()
    
    if os.path.exists(csv_filepath):
        with open(csv_filepath, "r+") as f:
            rows = f.readlines()            
            
            if rows:
                last_row = rows[-1].strip()  # Get the last row       
                
                if last_row.endswith(","):  # Check if `time_spent` is not already recorded
                    
                    # Extract the timestamp from the last row
                    try:
                        last_timestamp = float(last_row.split(",")[0])                        
                    except (IndexError, ValueError):
                        print("Error parsing last row for timestamp.")
                        return
                    
                    # Calculate time spent
                    time_spent = current_timestamp - last_timestamp                    
                    updated_last_row = f"{last_row} {time_spent:.2f}\n"                    
                    rows[-1] = updated_last_row  # Update the last row
                    
                    # Rewrite the file with the updated last row
                    f.seek(0)
                    f.writelines(rows)
                    f.truncate()
                    print(f"Time spent {time_spent:.2f} seconds recorded for the last URL.")
            else:
                print("CSV file is empty. No rows to update.")
    else:
        print(f"{csv_filepath} does not exist. Cannot record time spent.")


    ''' Identify the last page number '''
    # Path to the 'data' folder
    data_folder = "data"
    
    # List all files in the 'data' folder
    files = os.listdir(data_folder)
    
    # Filter for mouseX.csv files
    mouse_files = [f for f in files if f.startswith("mouse") and f.endswith(".csv")]
    
    # No mouseX.csv files found, return 1
    if not mouse_files:  
        return 1
    
    # Extract the numbers from the file names (e.g., mouse1.csv -> 1)
    page_numbers = []
    for file in mouse_files:
        try:
            # Extract the number between 'mouse' and '.csv'
            number = int(file[5:-4])
            page_numbers.append(number)
        except ValueError:
            continue  # Skip files that don't match the expected format
    
    # If no valid page numbers were found, return 1
    if not page_numbers:
        return 1
    
    # Find the maximum page number and add 1
    final_page_number = int(max(page_numbers))

    # Generate heatmap
    csv_filepath = f"data/mouse{final_page_number}.csv"
    if os.path.exists(csv_filepath):
        df = pd.read_csv(csv_filepath)

        # Calculate figsize
        fig_width_inch = screen_width / 100  # Scale down by 100 DPI
        fig_height_inch = screen_height / 100

        fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch))  # Set size to screen resolution
        fig.patch.set_alpha(0)  # Make transparent
        ax.patch.set_alpha(0)  # Make transparent
        ax.invert_yaxis()  # Invert y-axis to match the coordinate system of the recorded data

        # Create a KDE plot on the specified axes
        sns.kdeplot(
            x=df['x'], y=df['y'], cmap='viridis', fill=True, ax=ax,
            clip=((screen_width, 0), (0, screen_height))
        )
        
        # Remove axis labels and ticks
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_xticks([])
        ax.set_yticks([])

        # Ensure x and y axes have the same scale
        ax.set_aspect('equal', adjustable='box')

        # Remove the spines (borders) around the plot
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Adjust the layout to remove extra padding
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Save heatmap
        heatmap_path = f'static/data/heatmap_page{final_page_number}.png'
        plt.savefig(heatmap_path, transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        print(f"Heatmap saved to {heatmap_path}.")

    else:
        print(f"FINAL HEATMAP FAILED TO GENERATE")
    
    try:
        results_path = os.path.abspath("templates/show_results.html")  # Path to the HTML file
        if os.path.exists(results_path):
            webbrowser.open(f"http://127.0.0.1:3000/show_results")  # Open the Flask-hosted results
        else:
            messagebox.showerror("Error", "Results file not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open results. Error: {e}")

# Function to stop the Flask server when the GUI is closed
def on_closing():
    if flask_process:
        flask_process.terminate()
        print("Flask server stopped.")
    root.destroy()

# Function to center the window
def center_window(window):
    window.update_idletasks()  # Ensure the window dimensions are updated
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Calculate position
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the window position
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Initialize the GUI
root = tk.Tk()
root.title("Cursor Tracker")

# Set font styles
header_font = font.Font(family="Arial", size=16, weight="bold", slant="italic")
label_font = font.Font(family="Arial", size=12, weight="bold")
button_font = font.Font(family="Arial", size=12, weight="bold")

# Header
header = tk.Label(
    root, 
    text="Cursor Tracker", 
    font=header_font, 
    bg="#471164", 
    fg="white"
)
header.pack(fill="x", ipady=10)  # 'fill="x"' makes the background span the width of the GUI

# URL Entry Field
tk.Label(root, text="", font=label_font).pack(pady=0)  # to add space below header
tk.Label(root, text="Enter URL:", font=label_font).pack(pady=10)
url_entry = tk.Entry(root, width=40, font=('Arial 12'))
url_entry.pack(pady=5)
url_entry.pack(padx=20)

# Button Frame (to align buttons in a single row)
button_frame = tk.Frame(root)
button_frame.pack(pady=25)

# Start Button (Green)
start_button = tk.Button(
    button_frame, text="          Start          ", command=start_recording, bg="green", fg="white", font=button_font
)
start_button.pack(side="left", padx=25)

# Stop Button (Red)
stop_button = tk.Button(
    button_frame, text="          Stop          ", command=stop_recording, bg="red", fg="white", font=button_font
)
stop_button.pack(side="left", padx=25)

# Start the Flask server in a separate thread
server_thread = threading.Thread(target=start_flask_server, daemon=True)
server_thread.start()

# Handle GUI close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Center the window after it is created
root.update_idletasks()  # Ensure all widgets are rendered
center_window(root)

# Run the GUI
root.mainloop()