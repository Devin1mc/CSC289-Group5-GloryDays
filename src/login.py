from flask import Blueprint, render_template, request, redirect, session, url_for
import sqlite3
import hashlib

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

def setup_database():
    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@auth_bp.route("/")
def login_page():
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/login", methods=["POST"])
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
        # Save the user in session before redirecting
        session["user"] = employee_id
        session["role"] = result[1]
        return redirect(url_for("auth.inventory_page"))
    else:
        return "Invalid Employee ID or Password."

@auth_bp.route("/register", methods=["POST"])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    employee_id = request.form["employee_id"]
    password = request.form["password"]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    role = request.form.get("role", "user") #Get role from form, default to user.

    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, employee_id, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, employee_id, password_hash, role),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("auth.login_page"))
    except sqlite3.IntegrityError:
        return "Employee ID already exists."

@auth_bp.route("/inventory")
def inventory_page():
    if "user" in session:
        # Ensure the inventory template name matches your actual file (changed to inventory.html)
        return render_template("inventory.html")
    else:
        return redirect(url_for("auth.login_page"))

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login_page"))
