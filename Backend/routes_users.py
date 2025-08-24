# routes_users.py
from flask import Blueprint, jsonify
import csv

users_bp = Blueprint("users", __name__)

@users_bp.route("/all")
def list_users():
    users_list = []

    # Read CSV file
    with open("attendance.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_info = f"{row['First']} {row['Last']}, Age: {row['Age']}"
            users_list.append(user_info)

    return jsonify({"users": users_list})
