# Developer Documentation


## Overview
Cursor Tracker consists of a browser extension and two Python files that together track the movements of the user's cursor. The web pages visited, time spent on each web page, size of the monitor, and time stamps are also recorded. Screenshots of the visited web pages are taken. Using the data gathered, a heat map is generated for each visited web page, showing the user's cursor movements. The results are displayed in the browser, showing the web page screenshots with the associated heatmap overlayed. Below this, a bar chart that shows the time spent on each web page is generated.


## Final Planning Specs
The following are parts of the initial specs are currently implemented:
- Cursor movements are tracked and the "x" and "y" positions are recorded to a CSV
- A new CSV is created for each web page visited
- When a link is clicked, the URL and a timestamp are recorded
- The time spent on each web page is calculated using the timestamps
- A screenshot is taken of each web page visited
- A transparent heatmap is generated for each web page visited, based on the cursor movement data
- The screenshot and heatmap for each web page are overlayed
- The size of the user's monitor is recorded to enable the heatmap to accurately overlay the web page screenshot
- Users can toggle between the different web pages they visited while the tracking was active
- A bar chart is generated based on the URL data and time spent on each web page data
- A GUI starts and stops the application
- The user determines what web page to start the tracking on
- A local server is hosted while the application is running
- When the Cursor Tracker extension icon is clicked on in Google Chrome's toolbar, the browser extension overlays a small window with a tip on how to use Cursor Tracker


## Install/deployment/admin issues:
- It is possible to see the result of the previous recording after closing Cursor Tracker. The user has to change "1" to "0" in line 42 of "app.py", save, run "run_me.py", and then press the GUI's "Stop" button. This will display the results from the previous recording. If the user wants to start a new recording, close the GUI, change "0" back to "1" in line 42 of "app.py", and save. Now Cursor Tracker can be run like normal.
- To give the browser time to load a web page, the code waits 1 second after the "Start" button (in the GUI) is pressed before taking the screenshot of the first webpage. Then, a 0.5 second pause happens before taking a screenshot of each subsequent web page. This means if the user navigates to a new web page very rapidly, or a webpage takes a significant time to load, the screenshot may be inaccurate.
  - To change the delay of the first screenshot, go to line 90 in "run_me.py"
  - To change the delay of all the other screenshots, go to line 229 in "app.py"


## End User Interaction and Flow Through Code (Walkthrough)
- The user runs  "run_me.py"
  - The GUI appears, the Flask server is started, and data from the previous recording is deleted
    - run_me.py > start_recording()
- The user types the URL of where they wish to begin into the text box in the GUI
- User presses the "Start" button
	- The URL entered and a time stamp are recorded to "URL_clicks.csv"
		- run_me.py > start_recording()
	- "mouse1.csv" is created
		- run_me.py > start_recording()
	- In "mouse1.csv" the header text (needed for the heatmap generation) is entered, the upper left and lower right positions are entered (based on the user's screen size), and then the cursor coordinates start being written to it
		- app.py > track_mouse()
		- app.py > start()
	- A screenshot of the webpage is taken and named
		- run_me.py > start_recording()
- The user clicks on a link, navigating to a new web page
	- The URL and a time stamp are logged to "URL_clicks.csv"
		- app.py > new_url()
	- The time spent on the previous web page is calculated, and then entered into the previous row
		- app.py > new_url()
	- A screenshot of the new web page is taken
		- app.py > new_url()
	- A heatmap of the previous web page is rendered
		- app.py > new_url()
- User continues navigating to new web pages
	- *repeat of previous section*
- User concludes their testing, so they pull up the GUI and press the "Stop" button
	- The time spent on the last web page is calculated and entered into the last row in URL_clicks.csv
		- run_me.py > stop_recording()
		- app.py > end_session()
	- The final page number is identified
		- run_me.py > stop_recording()
	- The heatmap for the last web page is generated
		- run_me.py > stop_recording()
	- The Flask-hosted "results.html" file is opened in the browser
		- run_me.py > stop_recording()
- The results of the tracking appear in a new browser tab
	- The screenshots, heatmaps, and bar chart are loaded
		- run_me.py > stop_recording()
		- app.py > index()
		- app.py > show_results()
		- app.py > get_image_list()
		- app.py > get_click_data()
- The user is done analyzing the results and closes out of the browser
- The user closes the GUI window
	- The Flask server stops and the GUI is closed
		- run_me.py > on_closing()


## Known Issues
### Minor:
 - The following warning message appears "UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail."
 - Having to pull up the Cursor Tracker GUI to stop the recording could be seen as a negative if the cursor movements on the final web page is important.
 - Rapidly navigating to new web pages may not give the code enough time to take screenshots or generate heatmaps

### Major:
- Cursor Tracker cannot accurately display the cursor position if the user scrolls on a web page. If the user scrolls, the cursor position and screenshot are still recorded, but the heatmap will not be an accurate representation.
- Sometimes the URL of a new web page is not recorded. I have put much effort into trying to fix this but I still am not fully sure why this happens.

### Suspected computational inefficiencies:
- Currently, when a new web page is loaded, the heatmap for the previous webpage is rendered. This works, but it would probably be best to generate all the heatmaps at the end of the recording (when the GUI's "Stop" button is pressed) so that the heatmap generation does not slow down other processes.


## Future Work
- Making Cursor Tracker capable of recording data accurately when the user scrolls would greatly improve its usefulness. This includes taking a screenshot of the entire website (not what is just visible), and rendering the heatmap over the entire website.
- Fixing the issue where some URLs are not recorded would be a big improvement.
- If Cursor Tracker could identify when a web page is done loading and then take a screenshot, it would be an improvement over the current method of delaying the screenshot with a timer.
