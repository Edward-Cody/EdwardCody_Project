import subprocess
import webbrowser
import tkinter as tk
import requests
import threading
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyautogui # pip install pyautogui
from flask import jsonify
from tkinter import messagebox
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
            # messagebox.showinfo("Success", "Recording started, URL opened, and logged in CSV!")
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
'''
def final_page_number():
    # Path to the 'data' folder
    data_folder = "data"
    
    # List all files in the 'data' folder
    files = os.listdir(data_folder)
    
    # Filter for mouseX.csv files
    mouse_files = [f for f in files if f.startswith("mouse") and f.endswith(".csv")]
    
    if not mouse_files:
        # No mouseX.csv files found, return 1
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
    next_page_number = max(page_numbers)
    print(f"final page number: {next_page_number}")
    
    return next_page_number
'''
# Function to open the "show_results.html" file
def stop_recording():
    
    ''' Identify the last page number '''
    # Path to the 'data' folder
    data_folder = "data"
    
    # List all files in the 'data' folder
    files = os.listdir(data_folder)
    
    # Filter for mouseX.csv files
    mouse_files = [f for f in files if f.startswith("mouse") and f.endswith(".csv")]
    
    if not mouse_files:
        # No mouseX.csv files found, return 1
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
    next_page_number = int(max(page_numbers))

    # Generate heatmap
    csv_filepath = f"data/mouse{next_page_number}.csv"
    if os.path.exists(csv_filepath):
        df = pd.read_csv(csv_filepath)

        # Calculate figsize
        fig_width_inch = screen_width / 100  # Scale down by 100 DPI
        fig_height_inch = screen_height / 100

        fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch))
        fig.patch.set_alpha(0)
        ax.patch.set_alpha(0)
        ax.invert_yaxis()

        sns.kdeplot(
            x=df['x'], y=df['y'], cmap='viridis', fill=True, ax=ax,
            clip=((screen_width, 0), (0, screen_height))
        )
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal', adjustable='box')

        # Remove the spines (borders) around the plot
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Adjust the layout to remove extra padding
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Save heatmap
        heatmap_path = f'static/data/heatmap_page{next_page_number}.png'
        plt.savefig(heatmap_path, transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        print(f"Heatmap saved to {heatmap_path}.")

    else:
        print(f"FINAL HEATMAP FAILED TO GENERATE")
    
    try:
        results_path = os.path.abspath("templates/show_results.html")  # Path to the HTML file
        if os.path.exists(results_path):
            webbrowser.open(f"http://127.0.0.1:3000/show_results")  # Open the Flask-hosted results
            # messagebox.showinfo("Results", "Results page opened in the browser!")
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

# Initialize the GUI
root = tk.Tk()
root.title("Localhost GUI")

# GUI Layout
tk.Label(root, text="Enter URL:").pack(pady=5)
url_entry = tk.Entry(root, width=40)
url_entry.pack(pady=5)

start_button = tk.Button(root, text="Start", command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_recording)
stop_button.pack(pady=10)

# Start the Flask server in a separate thread
server_thread = threading.Thread(target=start_flask_server, daemon=True)
server_thread.start()

# Handle GUI close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
root.mainloop()