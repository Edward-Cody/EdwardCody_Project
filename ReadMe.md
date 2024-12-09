# ReadMe (User Guide)
Cursor Tracker is a way for developers to analyze how users navigate through a website/web app being worked on by the developer. Cursor Tracker consists of a browser extension and two Python files that together track the movements of the user's cursor, the web pages visited, and time spent on each web page. The size of the monitor and time stamps are also recorded. Screenshots of the visited web pages are taken. Using this data, a heat map showing the user's cursor movements is generated for each web page visited. A bar chart is also generated that shows the time spent on each web page.


## Installation 
- You need non-standard packages to run my app.py and run_me.py
  - Open an OS terminal (e.g. cmd.exe or PowerShell)
  - Use pip to install the required third-party packages:  `pip --upgrade -r requirements.txt`
- Google Chrome needs to be set as your default browser
- Before the user can run Cursor Tracker, the Cursor Tracker browser extension needs to be installed in Google Chrome.
  - Click the extension button in the Google Chrome toolbar:
    - ![Screenshot 2024-12-08 145053](https://github.com/user-attachments/assets/e2bfa084-00db-46e8-8270-ba7c7dee4276)
  - Click "Manage extensions"
  - Click "Load unpacked"
  - Select the "browser_extension_chrome" folder
  - "Cursor Tracker 5.0" should now appear in the list of "All Extensions"
  - Click "Details"
  - Activate "Allow in Incognito"
- Cursor Tracker setup is complete


## Usage
How to run Cursor Tracker
- Open an OS terminal (e.g. cmd.exe or PowerShell)
- Use "cd" to jump to the project root folder (e.g. `cd /Users/YourName/Desktop/EdwardCody_CursorTrackerTool`)
- Run "run_me.py": `python run_me.py`
- A GUI will appear in the center of the screen
- Type in the URL of the web page where you would like to start
  - ![image](https://github.com/user-attachments/assets/f91b66e0-0617-442b-9f05-894f19fe237d)
- Press the "Start" button
- Navigate the webpage to meet your testing goal*
  - *Cursor Tracker is intended to be used as a way for developers to analyze how users navigate through the website/web app being worked on by the developer.
- When the goal is achieved or the testing is done, press the "Stop" button in the GUI
- The "results.html" page will appear
  - ![image](https://github.com/user-attachments/assets/ed7677fe-8b61-405e-86c4-f1a6a04a765b)
- Now your cursor movements and time spent on each web page can be analyzed
  - If multiple web pages were visited while the tracking was happening, you can select which web page you want to see with the cursor movement heatmap overlay
  - You can hover over the bars in the Time Spent bar chart to see exact times
  - ![image](https://github.com/user-attachments/assets/d7218410-9aba-4a31-89b8-c3a1cf9b6b70)
- When done, close out of the web page and close the Cursor Tracker GUI
  - ![image](https://github.com/user-attachments/assets/0400b55c-ca56-43dc-ba96-0044b607c4b7)


## Known Issues
- Sometimes the URL of a new web page is not recorded. I have put much effort into trying to fix this but I still am not fully sure why this happens.


## Limitations
- Cursor Tracker cannot accurately display the cursor position if the user scrolls on a web page. If the user scrolls, the cursor position and screenshot are still recorded, but the heatmap will not be an accurate representation.
- Cursor Tracker is made for Google Chrome, and is not expected, nor has it been tested, to work in other browsers.
- While it is possible to see the result of the previous run after closing Cursor Tracker, it cannot be accomplished solely through the GUI. The user has to change "1" to "0" in line 42 of "app.py", run "run_me.py", and then press the "Stop" button. It works, but it is not intuitive.


## Acknowledgments
Many thanks to Dr. Harding. Cursor Tracker turned out to be far more difficult to implement than expected and his help was instrumental.
