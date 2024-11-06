from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import logging
import time
import threading
import pyautogui
import os
from glob import glob

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
current_page_number = 0
page_number_lock = threading.Lock()

#CSV setup for 2560x1440 monitor
header = "x,y"
UL = "0,0"
UR = "2560,0"
LR = "2560,1440"
LL = "0,1440"

def track_mouse():
    global current_page_number
    try:
        while True:
            # print(f"x,y", file=f) # WHERE I LEFT OFF - TRYING TO ADD X,Y AT TOP OF CSV
            x, y = pyautogui.position()
            with page_number_lock:
                filename = f"data/mouse{current_page_number}.csv"
            # Check if file is empty and write header if it is
            if not os.path.exists(filename) or os.path.getsize(filename) == 0:
                with open(filename, "w") as f:
                    print(header, file=f)
                    print(UL, file=f)  #may not be needed?
                    print(UR, file=f)  #may not be needed?
                    print(LR, file=f)  #may not be needed?
                    print(LL, file=f)  #may not be needed?
            # Append the coordinates to the file
            with open(filename, "a+") as f:
                # print(f"{time.time()}, {x}, {y}", file=f) #with timestamps
                print(f"{x},{y}", file=f)
    except KeyboardInterrupt:
        print("Mouse tracking stopped.")

# mouse tracking in a separate thread
mouse_thread = threading.Thread(target=track_mouse)
mouse_thread.daemon = True  # This ensures the thread will exit when the main program exits

@app.route('/')
def index():
    if len(glob("static/data/*")) > 0: # if there are any image files in the static folder
        return redirect(url_for('show_results'))
    else:
        return render_template('index.html') # show the index page if there are no image files
    
    
@app.route('/start', methods=['GET'])
def start():
    global mouse_thread
    # Get the value of the URL from the query parameter
    url = request.args.get('url')
    if url:
        print(f'[{time.time()}] Received URL: {url} (no screenshot can be taken for this page)')
        
        # start thread if not already started
        if not mouse_thread.is_alive():
                mouse_thread.start()
        
        return redirect(url) # show that URL in the browser
    
    else:
        redirect(url_for('index')) # redirect to the index page if no URL is provided

@app.route('/new_url', methods=['POST'])
def new_url():
    print("new_url")
    global current_page_number
    data = request.get_json()
    url = data['url']
    print(f'[{time.time()}] Clicked URL: {url}')  # must use absolute timestamps to sync with the mouse mvt file
    # append to clicks.

    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    with page_number_lock:
        # needs to be under static folder so flask can show them later
        screenshot.save(f'static/data/screenshot_page{current_page_number+1}.png')

    with open("data/URL_clicks.csv", "a+") as f:
        print(f"{time.time()}, {url}", file=f)
    
    # Update the global variable with the new page number
    with page_number_lock:
        current_page_number += 1    
    
    return jsonify(status='success')

'''
@app.route('/stop', methods=['GET'])
def stop():
    print(request.args.get("action"))

    # Return a JSON response to the popup js which will redirect the user to the show_results page
    return jsonify(status='success', redirect_url=url_for('show_results'))
'''

@app.route('/show_results', methods=['GET'])
def show_results():

    # for each mouse coords other than 1 create a heatmap and composite it over the screenshot
    # save the results in the static folder as jpgs and change the code below to use jpgs
    # instead of pngs - done (11/1/24)

    os.chdir('static/data')
    image_files = glob('*.png')
    os.chdir('../..')
    print(image_files)
    return render_template('show_results.html', images=image_files)
  
if __name__ == '__main__':
    print('Click here to open the app: http://127.0.0.1:3000')
    app.run(port=3000)

