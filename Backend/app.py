from flask import Flask, jsonify, render_template
import csv, os

app = Flask(__name__, template_folder="templates")
# Logo URL variable
logo_url = "https://yourdomain.com/path/to/logo.png"  # change to your logo

# Home page
@app.route("/")
def home():
    return render_template("home.html", logo_url=logo_url)

# JSON API endpoint
@app.route("/attendance/list")
def list_attendance():
    csv_path = os.path.join(os.path.dirname(__file__), "attendance.csv")
    if not os.path.exists(csv_path):
        return jsonify({"error": "attendance.csv not found"}), 404

    attendance_list = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
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

# Attendance table page
@app.route("/attendance")
def attendance_table():
    csv_path = os.path.join(os.path.dirname(__file__), "attendance.csv")
    if not os.path.exists(csv_path):
        return "<h1>attendance.csv not found</h1>"

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    return render_template("attendance.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
