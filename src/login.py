from flask import Blueprint, render_template, request, redirect, session, url_for
import sqlite3
import hashlib

# Create a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Database connection
def get_user_connection():
    user_conn = sqlite3.connect("login_database.db")
    user_conn.row_factory = sqlite3.Row
    return user_conn

def setup_database():
    print("Running setup_database()...")  # ✅ Debugging statement
    user_conn = sqlite3.connect("login_database.db")
    cursor = user_conn.cursor()
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
    user_conn.commit()
    user_conn.close()
    print("Database setup complete!")  # ✅ Debugging statement

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

    user_conn = sqlite3.connect("login_database.db")
    cursor = user_conn.cursor()
    cursor.execute("SELECT first_name, last_name, password_hash, role FROM users WHERE employee_id = ?", (employee_id,))
    result = cursor.fetchone()
    user_conn.close()

    if result and password_hash == result[2]:
        # Store the user's full name and role in session
        session["user"] = employee_id
        session["first_name"] = result[0]
        session["last_name"] = result[1]
        session["role"] = result[3]
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
    role = request.form.get("role", "user")  # Get role from form, default to user.

    admin_id = request.form["admin_id"]
    admin_password = request.form["admin_password"]
    admin_password_hash = hashlib.sha256(admin_password.encode()).hexdigest()

    user_conn = sqlite3.connect("login_database.db")
    cursor = user_conn.cursor()

    # Check if the provided admin credentials are valid
    cursor.execute(
        "SELECT role, password_hash FROM users WHERE employee_id = ?", (admin_id,)
    )
    admin_data = cursor.fetchone()

    if not admin_data or admin_data[0] not in ["admin", "manager"] or admin_data[1] != admin_password_hash:
        user_conn.close()
        return "Invalid admin credentials or insufficient privileges."

    try:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, employee_id, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            (first_name, last_name, employee_id, password_hash, role),
        )
        user_conn.commit()
        user_conn.close()
        return redirect(url_for("auth.login_page"))
    except sqlite3.IntegrityError:
        return "Employee ID already exists."
    
@auth_bp.route("/inventory")
def inventory_page():
    if "user" in session:
        # Get the user's first and last name from the session
        first_name = session.get("first_name")
        last_name = session.get("last_name")
        
        # Pass the name to the template
        return render_template("inventory.html", first_name=first_name, last_name=last_name)
    else:
        return redirect(url_for("auth.login_page"))

@auth_bp.route("/logout")
def logout():
    session.clear()  # Clears the entire session
    return redirect(url_for("auth.login_page"))
