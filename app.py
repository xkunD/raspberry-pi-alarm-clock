import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
ALARM_FILE = "/home/pi/final_project/alarms.json"

def load_alarms():
    """Load alarms from the shared JSON file."""
    try:
        with open(ALARM_FILE, "r") as f:
            return json.load(f).get("alarms", [])
    except FileNotFoundError:
        return []

def save_alarms(alarms):
    """Save alarms to the shared JSON file."""
    with open(ALARM_FILE, "w") as f:
        json.dump({"alarms": alarms}, f)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/alarms', methods=['GET'])
def get_alarms():
    alarms = load_alarms()
    return jsonify({"alarms": alarms})

@app.route('/alarms', methods=['POST'])
def set_alarm():
    alarm_time = request.json.get('time')
    if alarm_time:
        alarms = load_alarms()
        alarms.append(alarm_time)
        save_alarms(alarms)
        return jsonify({"message": "Alarm added", "alarms": alarms})
    return jsonify({"error": "Invalid input"}), 400

@app.route('/alarms/<int:alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
    alarms = load_alarms()
    if 0 <= alarm_id < len(alarms):
        removed_alarm = alarms.pop(alarm_id)
        save_alarms(alarms)
        return jsonify({"message": "Alarm deleted", "removed_alarm": removed_alarm})
    return jsonify({"error": "Invalid alarm ID"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
