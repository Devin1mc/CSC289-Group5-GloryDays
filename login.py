import sqlite3
import hashlib

# Function to set up the database 
def setup_database():
    # Connecting to (or create) the login database
    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()

    # Creating the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            employee_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Commiting changes
    conn.commit()

    # Select and print all users
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(row)
    
    # Closing connection
    conn.close()
    print("Database and table setup complete.")

# Function to register a new user
def register_user(first_name, last_name, employee_id, password):
    # Hash the password using SHA-256
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Connecting to the database
    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()

    try:
        # Inserting new user into the database
        cursor.execute("INSERT INTO users (first_name, last_name, employee_id, password_hash) VALUES (?, ?, ?, ?)", 
                       (first_name, last_name, employee_id, password_hash))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Error: Employee ID already exists.")
    
    # Closing the connection
    conn.close()

# Function to verify login
def login_user(employee_id, password):
    # Hash the input password to compare with the stored hash
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Connecting to the database
    conn = sqlite3.connect("login_database.db")
    cursor = conn.cursor()

    # Retrieve the stored password hash for the given employee ID
    cursor.execute("SELECT password_hash FROM users WHERE employee_id = ?", (employee_id,))
    result = cursor.fetchone()

    # Checking if a matching user was found
    if result and password_hash == result[0]:
        print("Login successful!")
    else:
        print("Invalid credentials.")

    # Closing the connection
    conn.close()

    


if __name__ == "__main__":
    setup_database()  # Run this once to set up the database
    # Example usage below
    # Uncomment the following lines to test:
    # register_user("John", "Doe", "EMP001", "securepassword123")  # Register a test user
    # login_user("EMP001", "securepassword123")  # Correct password
    # login_user("EMP001", "wrongpassword")  # Incorrect password
    # login_user("EMP999", "anypassword")  # Non-existent employee ID
