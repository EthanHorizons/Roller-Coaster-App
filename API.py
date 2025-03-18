from flask import Flask, jsonify

import requests
import os
import secret
app = Flask(__name__)

url = "https://captaincoaster.com/api/coasters"

headers = {
    "accept": "application/ld+json",
    "Authorization": secret.grabkey()
}


#getting all coasters
@app.route('/fetch', methods=['GET'])
def fetch():
    response = requests.get(url, headers=headers)
    return jsonify(response.json())
#getting individual coasters
@app.route('/find/<int:coaster_id>', methods=['GET'])
def find(coaster_id):
    detailsURL = f"{url}/{coaster_id}"
    response = requests.get(detailsURL, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
            return jsonify({"error": f"Unexpected error: {response.status_code}"}), response.status_code
#searching named coaster
@app.route('/name/<string:name>', methods=['GET'])
def name(name):
    nameURL = f"{url}?page=1&name={name}&order%5Bid%5D=asc&order%5Brank%5D=asc"
    response = requests.get(nameURL, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5100)  

