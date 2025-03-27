import firebase_admin
from firebase_admin import credentials, db

# Firebase Initialization (Only Once)
cred = credentials.Certificate("D:/git/Bell-system/firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://bell-system-aiat-52f14-default-rtdb.asia-southeast1.firebasedatabase.app/holidays"
})

# Function to get holidays
def get_holidays():
    ref = db.reference("holidays")
    return ref.get() or {}

# Function to add a holiday
def add_holiday(date, description):
    ref = db.reference("holidays")
    ref.child(date).set({"description": description})

# Function to remove a holiday
def remove_holiday(date):
    ref = db.reference("holidays")
    if ref.child(date).get():
        ref.child(date).delete()
        return True
    return False
