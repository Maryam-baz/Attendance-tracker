from flask import Flask, render_template, request, redirect, url_for, session
import csv, os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

CSV_FILE = os.path.join(os.path.dirname(__file__), 'attendance.csv')
EMPLOYEE_PASSWORD = 'employee123'

# --- CSV read/write ---
def read_csv_file():
    students = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "First","Last","Age","Dropped off","Picked up","Emergency Name","Emergency Phone"
            ])
            writer.writeheader()
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            students.append({k.strip(): v.strip() for k, v in row.items()})
    return students

def write_csv_file(students):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["First","Last","Age","Dropped off","Picked up","Emergency Name","Emergency Phone"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for s in students:
            writer.writerow(s)

# --- Home ---
@app.route('/')
def home():
    return render_template('home.html')

# --- Employee login ---
@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == EMPLOYEE_PASSWORD:
            session['employee_logged_in'] = True
            return redirect(url_for('attendance'))
        else:
            error = "Incorrect password"
    return render_template('employee_login.html', error=error)

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('employee_logged_in', None)
    return redirect(url_for('home'))

# --- Attendance page ---
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    students = read_csv_file()
    is_employee = session.get('employee_logged_in', False)

    if request.method == 'POST':
        for i, student in enumerate(students):
            # Employee can edit all fields
            if is_employee:
                student['First'] = request.form.get(f'first_{i}')
                student['Last'] = request.form.get(f'last_{i}')
                student['Age'] = request.form.get(f'age_{i}')
                student['Emergency Name'] = request.form.get(f'emergency_name_{i}')
                student['Emergency Phone'] = request.form.get(f'emergency_phone_{i}')

            # Everyone can update dropped off/picked up
            student['Dropped off'] = 'Yes' if request.form.get(f'dropped_{i}') == 'Yes' else 'No'
            student['Picked up'] = 'Yes' if request.form.get(f'picked_{i}') == 'Yes' else 'No'

        # Only employees can add new students
        if is_employee:
            new_first = request.form.get('new_first')
            new_last = request.form.get('new_last')
            new_age = request.form.get('new_age')
            if new_first and new_last and new_age:
                students.append({
                    'First': new_first,
                    'Last': new_last,
                    'Age': new_age,
                    'Dropped off': 'Yes' if request.form.get('new_dropped') == 'Yes' else 'No',
                    'Picked up': 'Yes' if request.form.get('new_picked') == 'Yes' else 'No',
                    'Emergency Name': request.form.get('new_emergency_name', ''),
                    'Emergency Phone': request.form.get('new_emergency_phone', '')
                })

        write_csv_file(students)
        return redirect(url_for('attendance'))

    still_here = sum(1 for s in students if s["Dropped off"] == "Yes" and s["Picked up"] == "No")
    return render_template('attendance.html', rows=students, still_here=still_here, is_employee=is_employee)

if __name__ == "__main__":
    app.run(debug=True)