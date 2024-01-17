import os
from flask import Flask, jsonify, request, render_template  # pip install flask flask-socketio
from flask_socketio import SocketIO  # pip install flask-socketio
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Directory to store client data
CLIENT_DATA_DIR = 'client_data'

# Ensure the directory exists
os.makedirs(CLIENT_DATA_DIR, exist_ok=True)


# API endpoint to receive and save JSON
@app.route('/api/save_json', methods=['POST'])
def save_json():
    try:
        json_data = request.get_json()

        if not json_data:
            return jsonify({"error": "Empty JSON payload"}), 400

        filename = os.path.join(CLIENT_DATA_DIR, f"json_{len(os.listdir(CLIENT_DATA_DIR)) + 1}.json")

        with open(filename, 'w') as file:
            json.dump(json_data, file)

        # Emit real-time update to connected clients
        emit_saved_data()

        return jsonify({"message": "JSON data saved successfully", "filename": filename})

    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# API endpoint to retrieve saved JSON data
@app.route('/api/get_saved_data', methods=['GET'])
def get_saved_data():
    try:
        saved_data = []
        for filename in os.listdir(CLIENT_DATA_DIR):
            filepath = os.path.join(CLIENT_DATA_DIR, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                saved_data.append(data)

        return jsonify(saved_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@socketio.on('connect')
def handle_connect():
    emit_saved_data()


def emit_saved_data():
    saved_data = []
    for filename in os.listdir(CLIENT_DATA_DIR):
        filepath = os.path.join(CLIENT_DATA_DIR, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            saved_data.append(data)
    socketio.emit('update_saved_data', saved_data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
