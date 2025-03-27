from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import backend  # Import Firebase functions from backend.py

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Firebase API Key for Authentication
FIREBASE_WEB_API_KEY = "AIzaSyDi_GZDf1Gx6mPStqyGwJ1CwLD2bfr9x6Q"

# Serve Frontend
@app.route('/')
def index():
    return render_template("index.html")

# Login Route (Using Firebase Authentication API)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Login successful", "data": response.json()})
    return jsonify({"status": "error", "message": "Invalid email or password"}), 401

# Fetch Holidays
@app.route('/get_holidays', methods=['GET'])
def get_holidays():
    holidays = backend.get_holidays()
    return jsonify(holidays)

# Add Holiday
@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    data = request.json
    date = data.get("date")
    description = data.get("description")

    if not date or not description:
        return jsonify({"status": "error", "message": "Date and description required"}), 400

    backend.add_holiday(date, description)
    return jsonify({"status": "success", "message": "Holiday added"})

# Remove Holiday
@app.route('/remove_holiday', methods=['POST'])
def remove_holiday():
    data = request.json
    date = data.get("date")

    if backend.remove_holiday(date):
        return jsonify({"status": "success", "message": "Holiday removed"})
    return jsonify({"status": "error", "message": "Holiday not found"}), 404

# Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
