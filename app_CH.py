from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from any origin

# Disable Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/new_url', methods=['POST'])
def new_url():
    data = request.get_json()
    url = data['url']
    print(f'[{time.time()}] Clicked URL: {url}') # must use absolute timestamps to sync with the mouse mvt file
    # append to clicks.
    with open("URL_clicks.csv", "a+") as f:
        print(f"{time.time()}, {url}", file=f)
    return jsonify(status='success')

if __name__ == '__main__':
    print('Server running on port 3000')
    app.run(port=3000)