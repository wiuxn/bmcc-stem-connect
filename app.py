from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            major TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            position TEXT,
            location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            internship_id INTEGER,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(internship_id) REFERENCES internships(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    major = request.form['major']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, major) VALUES (?, ?, ?)", (name, email, major))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    name = request.form['name']
    email = request.form['email']
    major = request.form['major']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, email=?, major=? WHERE id=?", (name, email, major, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/internships')
def internships():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()
    conn.close()
    return render_template('internships.html', internships=internships)

@app.route('/add_internship', methods=['POST'])
def add_internship():
    company = request.form['company']
    position = request.form['position']
    location = request.form['location']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO internships (company, position, location) VALUES (?, ?, ?)", (company, position, location))
    conn.commit()
    conn.close()
    return redirect('/internships')

@app.route('/delete_internship/<int:id>')
def delete_internship(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM internships WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/internships')

@app.route('/applications')
def applications():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()

    cursor.execute("""
        SELECT applications.id, students.name, internships.company, internships.position, applications.status
        FROM applications
        JOIN students ON applications.student_id = students.id
        JOIN internships ON applications.internship_id = internships.id
    """)
    applications = cursor.fetchall()

    conn.close()
    return render_template('applications.html', students=students, internships=internships, applications=applications)

@app.route('/add_application', methods=['POST'])
def add_application():
    student_id = request.form['student_id']
    internship_id = request.form['internship_id']
    status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO applications (student_id, internship_id, status) VALUES (?, ?, ?)", (student_id, internship_id, status))
    conn.commit()
    conn.close()
    return redirect('/applications')

@app.route('/delete_application/<int:id>')
def delete_application(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/applications')
@app.route('/edit_internship/<int:id>')
def edit_internship(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM internships WHERE id = ?", (id,))
    internship = cursor.fetchone()

    conn.close()
    return render_template('edit_internship.html', internship=internship)

@app.route('/update_internship/<int:id>', methods=['POST'])
def update_internship(id):
    company = request.form['company']
    position = request.form['position']
    location = request.form['location']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE internships
        SET company=?, position=?, location=?
        WHERE id=?
    """, (company, position, location, id))

    conn.commit()
    conn.close()

    return redirect('/internships')
@app.route('/edit_application/<int:id>')
def edit_application(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applications WHERE id = ?", (id,))
    application = cursor.fetchone()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM internships")
    internships = cursor.fetchall()

    conn.close()

    return render_template(
        'edit_application.html',
        application=application,
        students=students,
        internships=internships
    )


@app.route('/update_application/<int:id>', methods=['POST'])
def update_application(id):

    student_id = request.form['student_id']
    internship_id = request.form['internship_id']
    status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET student_id=?, internship_id=?, status=?
        WHERE id=?
    """, (student_id, internship_id, status, id))

    conn.commit()
    conn.close()

    return redirect('/applications')
if __name__ == '__main__':
    app.run(debug=True)