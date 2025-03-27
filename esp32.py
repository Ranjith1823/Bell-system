from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db
import requests

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Firebase Initialization
cred = credentials.Certificate("C:/Users/ranji/Downloads/New folder/Bell-system/bell-system-aiat-25b6a-firebase-adminsdk-fbsvc-f32db63123.json")  # Ensure the file is in the same directory
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://bell-system-aiat-25b6a-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Firebase API Key for Authentication
FIREBASE_WEB_API_KEY = "AIzaSyDKrb8bkzGh9D84EjNeE5vjh-b2LLB57nU"

# Serve Frontend
@app.route('/')
def index():
    return render_template("index.html")  # Ensure index.html is inside the same directory

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
    ref = db.reference("holidays")
    holidays = ref.get()
    return jsonify(holidays if holidays else {})

# Add Holiday
@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    data = request.json
    date = data.get("date")
    description = data.get("description")

    if not date or not description:
        return jsonify({"status": "error", "message": "Date and description required"}), 400

    ref = db.reference("holidays")
    ref.child(date).set({"description": description})
    
    return jsonify({"status": "success", "message": "Holiday added"})

# Remove Holiday
@app.route('/remove_holiday', methods=['POST'])
def remove_holiday():
    data = request.json
    date = data.get("date")

    ref = db.reference("holidays")
    if ref.child(date).get():
        ref.child(date).delete()
        return jsonify({"status": "success", "message": "Holiday removed"})
    else:
        return jsonify({"status": "error", "message": "Holiday not found"}), 404

# Run Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

