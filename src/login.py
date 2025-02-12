from flask import Flask, render_template, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

# Function to create the database (only runs once)
def setup_database():
    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to serve the login page
@app.route("/")
def login_page():
    return render_template("login.html")

# Route to serve the register page
@app.route("/register")
def register_page():
    return render_template("register.html")

# Route to handle login form submission
@app.route("/login", methods=["POST"])
def login():
    employee_id = request.form["employee_id"]
    password = request.form["password"]
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE employee_id = ?", (employee_id,))
    result = cursor.fetchone()
    conn.close()

    if result and password_hash == result[0]:
        return render_template("inventory.html")

    else:
        return "Invalid Employee ID or Password."

# Route to handle user registration
@app.route("/register", methods=["POST"])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    employee_id = request.form["employee_id"]
    password = request.form["password"]
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (first_name, last_name, employee_id, password_hash) VALUES (?, ?, ?, ?)", 
                       (first_name, last_name, employee_id, password_hash))
        conn.commit()
        conn.close()
        return redirect("/")
    except sqlite3.IntegrityError:
        return "Employee ID already exists."
    
# Route for inventory page
@app.route("/inventory")
def inventory_page():
    if "user" in session:  # Check if user is logged in
        return render_template("inventory-html.html")
    else:
        return redirect(url_for("login_page"))
    
# Route for logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    setup_database()  # Run once to set up the database
    app.run(debug=True)
