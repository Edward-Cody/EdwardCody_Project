from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import time

app = Flask(__name__)
CORS(app)

# Disable Flask's default logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

start = time.time()

@app.route('/new_url', methods=['POST'])
def new_url():
    data = request.get_json()
    url = data['url']
    timestamp = time.time() - start # High-resolution timestamp
    print(f'[{timestamp}] Clicked URL: {url}')
    with open("URL_clicks.csv", "a+") as f:
        print(f"{time.time()}, {url}", file=f)
    return jsonify(status='success')

@app.route('/click', methods=['POST'])
def click():
    timestamp = time.time() - start # High-resolution timestamp
    print(f'[{timestamp}] click')

    return jsonify(status='success')
@app.route('/write_coordinates', methods=['POST'])
def write_coordinates():
    data = request.get_json()
    x = data['x']
    y = data['y']
    timestamp = time.time() - start  # High-resolution timestamp
    print(f'[{timestamp}] x: {x}, y: {y}')
    #with open('coordinates.txt', 'a') as f:  # append to file
    #    f.write(f'{timestamp},{x},{y}\n')
    return jsonify(status='success')

#CAN DELETE
if __name__ == '__main__':
    print('Server running on port 3000')
    app.run(port=3000)
    #app.run(port=3000, ssl_context=('cert.pem', 'key.pem')) # run as https