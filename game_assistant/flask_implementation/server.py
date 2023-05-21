from flask import Flask, render_template, jsonify, request
import requests
import os
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder = TEMPLATE_DIR)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get-started', methods=['GET'])
def get_started():
    return render_template('get_started.html')

@app.route('/lore', methods=['POST'])
def lore():
    payload = request.get_json()
    print("Received payload:", payload)  # Print the received payload
    print(f"Generate a game description about a game called {payload['game_name']} about a " \
          f"character name {payload['main_character_name']} where the theme and " \
          f"genre are {payload['theme']} and {payload['genre']}.")
    # Send the payload to the external URL
    response = requests.post('<external_url_here>', json=payload)
    if response.status_code == 200:
        return jsonify({"message": "Lore created and sent successfully"})
    else:
        return jsonify({"message": "Failed to create and send lore"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)