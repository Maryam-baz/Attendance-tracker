from flask import Blueprint, jsonify
import csv
import os

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/summary")
def attendance_report():
    report_list = []

    # Use absolute path to avoid file-not-found errors
    csv_path = os.path.join(os.path.dirname(__file__), "attendance.csv")
    
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert Yes/No to 1/0
                dropped_off = 1 if row['Dropped off'].strip().lower() == 'yes' else 0
                picked_up = 1 if row['Picked up'].strip().lower() == 'yes' else 0

                student_report = {
                    "First": row['First'],
                    "Last": row['Last'],
                    "Age": row['Age'],
                    "Dropped_off": dropped_off,
                    "Picked_up": picked_up,
                    "Emergency_Contact_Name": row['Emergency Contact Name'],
                    "Emergency_Contact_Phone": row['Emergency Contact Phone']
                }

                report_list.append(student_report)
    except FileNotFoundError:
        return jsonify({"error": "attendance.csv not found"}), 404
    except KeyError as e:
        return jsonify({"error": f"Missing column in CSV: {e}"}), 400

    return jsonify({"report": report_list})
