from flask import Flask, jsonify
import csv
import os

app = Flask(__name__)

@app.route("/attendance/list")
def list_attendance():
    attendance_list = []

    # Use absolute path to ensure CSV is found
    csv_path = os.path.join(os.path.dirname(__file__), "attendance.csv")
    if not os.path.exists(csv_path):
        return jsonify({"error": "attendance.csv not found"}), 404

    # Read CSV and append each row to the list
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            attendance_list.append({
                "First": row.get("First", ""),
                "Last": row.get("Last", ""),
                "Age": row.get("Age", ""),
                "Dropped_off": row.get("Dropped off", ""),
                "Picked_up": row.get("Picked up", ""),
                "Emergency_Contact_Name": row.get("Emergency Contact Name", ""),
                "Emergency_Contact_Phone": row.get("Emergency Contact Phone", "")
            })

    # Return the full list inside a single JSON object
    return jsonify({"attendance": attendance_list})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
