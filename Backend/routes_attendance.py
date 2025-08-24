from flask import Flask, jsonify
import csv, os

app = Flask(__name__)

@app.route("/attendance/list")
def list_attendance():
    csv_path = os.path.join(os.path.dirname(__file__), "attendance.csv")
    if not os.path.exists(csv_path):
        return jsonify({"error": "attendance.csv not found"}), 404

    attendance_list = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')  # make sure delimiter is comma
        for row in reader:
            # strip all values to remove extra spaces
            attendance_list.append({
                "First": row.get("First", "").strip(),
                "Last": row.get("Last", "").strip(),
                "Age": row.get("Age", "").strip(),
                "Dropped_off": row.get("Dropped off", "").strip(),
                "Picked_up": row.get("Picked up", "").strip(),
                "Emergency_Contact_Name": row.get("Emergency Contact Name", "").strip(),
                "Emergency_Contact_Phone": row.get("Emergency Contact Phone", "").strip()
            })

    return jsonify({"attendance": attendance_list})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
