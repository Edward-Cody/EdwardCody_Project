import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import pyautogui # pip install pyautogui  
import pygetwindow as gw # pip install pygetwindow
import seaborn as sns
import subprocess
import threading
import time
import tkinter as tk
import requests
import webbrowser
import win32gui # pip install pywin32

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from glob import glob
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pynput import mouse # pip install pynput
from screeninfo import get_monitors
from tkinter import messagebox


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

# Disable Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# make a data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('static/data'):
    os.makedirs('static/data')

# set this to 1 to start a new recording run
# set this to 0 to see the results of the previous run
if 1:
    for file in os.listdir('data'):os.remove(f'data/{file}')
    for file in os.listdir('static/data'):os.remove(f'static/data/{file}')
    print("All files in data folder removed, beginning new recording")

# Global variable to store the URL
current_page_number = 1
page_number_lock = threading.Lock()

# Get screen dimensions
screen = get_monitors()[0]  # Assumes a single monitor setup; otherwise specify the desired monitor
screen_width = screen.width
screen_height = screen.height
screen_width_str = str(screen_width)
screen_height_str = str(screen_height)

# CSV setup for user's monitor size
header = "x,y"
UL = "0,0"
LR = screen_width_str+","+screen_height_str

# Record mouse coordinates in CSV
def track_mouse():
    global current_page_number
    try:
        while True:
            x, y = pyautogui.position()
            with page_number_lock:
                filename = f"data/mouse{current_page_number}.csv"
            
            # Check if file is empty and write header if it is
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                with open(filename, "w") as f:
                    print(header, file=f)  # required for heatmap processing
                    print(UL, file=f)  # needed so that screenshot matches screensize, making heatmap accurate
                    print(LR, file=f)  # needed so that screenshot matches screensize, making heatmap accurate
            
            # Append the coordinates to the file
            with open(filename, "a+") as f:
                print(f"{x},{y}", file=f)
    except KeyboardInterrupt:
        print("Mouse tracking stopped.")

# mouse tracking in a separate thread
mouse_thread = threading.Thread(target=track_mouse)
mouse_thread.daemon = True  # This ensures the thread will exit when the main program exits


@app.route('/')
def index():
    if len(glob("static/data/*")) > 0:  # if there are any image files in the static folder
        return redirect(url_for('show_results'))
    else:
        return render_template('error')  # show the index page if there are no image files
    
    
@app.route('/start', methods=['GET'])
def start():
    global mouse_thread
    
    # Get the value of the URL from the query parameter
    url = request.args.get('url')
    if url:
        print(f'[{time.time()}] Starting URL: {url}')  # Log the URL click
    
        # start thread if not already started
        if not mouse_thread.is_alive():
                mouse_thread.start()
        return redirect(url)  # show that URL in the browser

# Global variables to track the previous URL and timestamp
previous_timestamp = None
previous_url = None

@app.route('/new_url', methods=['POST'])
def new_url():
    global current_page_number, previous_timestamp, previous_url

    # Get JSON payload
    data = request.get_json()

    # Validate JSON and 'url' key
    if not data or 'url' not in data:
        print("Invalid request: 'url' key missing or malformed JSON")
        return jsonify(status='error', message="'url' key missing or invalid JSON"), 400

    url = data['url']
    current_timestamp = time.time()
    print(f'[{current_timestamp}] Clicked URL: {url}')  # Log the URL click

    # Calculate time spent and update the first row
    csv_filepath = "data/URL_clicks.csv"
    if previous_timestamp is None and previous_url is None:
        # Handle the first row case
        with open(csv_filepath, "r+") as f:
            rows = f.readlines()
            if rows:
                # Update the first row with calculated time_spent
                first_row = rows[0].strip()
                timestamp_in_first_row = float(first_row.split(",")[0])  # Extract the timestamp
                time_spent = current_timestamp - timestamp_in_first_row
                updated_first_row = f"{first_row} {time_spent:.2f}\n"
                rows[0] = updated_first_row

                # Rewrite the file with the updated first row
                f.seek(0)
                f.writelines(rows)
                f.truncate()

    elif previous_timestamp is not None and previous_url is not None:
        # Handle subsequent rows
        time_spent = current_timestamp - previous_timestamp

        # Update the last logged row
        with open(csv_filepath, "r+") as f:
            rows = f.readlines()
            if rows:
                last_row = rows[-1].strip()
                if last_row.endswith(","):  # Check if the last row is incomplete
                    updated_last_row = f"{last_row} {time_spent:.2f}\n"
                    rows[-1] = updated_last_row

                # Rewrite the file with the updated rows
                f.seek(0)
                f.writelines(rows)
                f.truncate()

    # Log the new URL with a placeholder for time spent
    with open(csv_filepath, "a+") as f:
        f.write(f"{current_timestamp}, {url}, \n")

    # Update globals for the next URL
    previous_timestamp = current_timestamp
    previous_url = url

    # Screenshot logic
    try:
        with page_number_lock:
            screenshot = pyautogui.screenshot()
            screenshot_path = f'static/data/screenshot_page{current_page_number + 1}.png'
            screenshot.save(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}.")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return jsonify(status='error', message="Failed to take screenshot"), 500

    # Heatmap generate logic
    csv_filepath = f"data/mouse{current_page_number}.csv"
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
        heatmap_path = f'static/data/heatmap_page{current_page_number}.png'
        plt.savefig(heatmap_path, transparent=True, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

        print(f"Heatmap saved to {heatmap_path}.")

    else:
        print(f"No mouse data found for page {current_page_number}.")

    with page_number_lock:
        current_page_number += 1

    return jsonify(status='success')

@app.route('/end_session', methods=['POST'])
def end_session():
    """Handles session end to log the time spent on the last page."""
    global previous_timestamp, previous_url

    if previous_timestamp is not None and previous_url is not None:
        current_timestamp = time.time()
        time_spent = current_timestamp - previous_timestamp

        # Log the last URL and time spent to CSV
        with open("data/URL_clicks.csv", "a+") as f:
            f.write(f"{previous_timestamp}, {previous_url}, {time_spent:.2f}\n")
        print(f"Session ended. Last page logged with {time_spent:.2f} seconds spent.")

    # Reset globals
    previous_timestamp = None
    previous_url = None

    return jsonify(status='success', message='Session ended and time logged.')


@app.route('/show_results', methods=['GET'])
def show_results():

    # for each mouse coords create a heatmap and composite it over the screenshot
    # save the results in the static folder as pngs
    os.chdir('static/data')
    image_files = glob('*.png')
    os.chdir('../..')
    print(image_files)
    return render_template('show_results.html', images=image_files)


@app.route('/static/data', methods=['GET'])
def get_image_list():
    files = glob('static/data/*.png')
    # Filter out "page0" or any invalid pages
    valid_files = [os.path.basename(f) for f in files if "page0" not in f]
    return jsonify(valid_files)


@app.route('/get_click_data', methods=['GET'])
def get_click_data():
    csv_filepath = "data/URL_clicks.csv"
    try:
        # Read CSV and extract URL and time_spent
        df = pd.read_csv(csv_filepath, header=None, names=["timestamp", "url", "time_spent"])
        df = df.dropna()  # Drop rows with missing time_spent
        data = df[["url", "time_spent"]].to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    print('Click here to open the app: http://127.0.0.1:3000')
    app.run(port=3000)