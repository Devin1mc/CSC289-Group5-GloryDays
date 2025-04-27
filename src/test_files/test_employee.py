import unittest
import os
import sqlite3
import hashlib
import sys

# Add src/ to the Python path
current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(src_dir)

# These is one folder up from test_files
from login import setup_database
from app import app


class TestEmployeeDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database file for testing employee logic.
        self.test_db = "test_login_database.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        # Monkey-patch sqlite3.connect in the login module to use the test DB.
        import login
        self.original_connect = sqlite3.connect
        sqlite3.connect = lambda db, **kwargs: self.original_connect(self.test_db, **kwargs)
        
        # Initialize the employee database.
        setup_database()
        
        # Insert an admin user so that registration can succeed.
        admin_pass = "adminpass"
        admin_hash = hashlib.sha256(admin_pass.encode()).hexdigest()
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, employee_id, password_hash, role) VALUES (?, ?, ?, ?, ?)",
            ("Admin", "User", "admin1", admin_hash, "admin")
        )
        conn.commit()
        conn.close()
        
        # Create the Flask test client.
        self.client = app.test_client()

    def tearDown(self):
        # Restore the original sqlite3.connect function.
        sqlite3.connect = self.original_connect
        # Remove the temporary test database file.
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_register_and_login(self):
        print("Running test_register_and_login: Testing registration and login workflow.")

        # --- Registration Test ---
        print("Step 1: Testing registration...")
        register_response = self.client.post("/register", data={
            "first_name": "John",
            "last_name": "Doe",
            "employee_id": "emp123",
            "password": "password123",
            "admin_id": "admin1",
            "admin_password": "adminpass"
        }, follow_redirects=True)
        self.assertEqual(register_response.status_code, 200)
        print("PASS: Registration succeeded.")

        # --- Valid Login Test ---
        print("Step 2: Testing login with correct credentials...")
        login_response = self.client.post("/login", data={
            "employee_id": "emp123",
            "password": "password123"
        }, follow_redirects=True)
        # Check for the presence of the registered user's first name in the response.
        self.assertIn(b"John", login_response.data)
        print("PASS: Login with correct credentials succeeded.")

        # --- Invalid Login Test ---
        print("Step 3: Testing login with incorrect password...")
        bad_login = self.client.post("/login", data={
            "employee_id": "emp123",
            "password": "wrongpassword"
        }, follow_redirects=True)
        self.assertIn(b"Invalid Employee ID or Password.", bad_login.data)
        print("PASS: Login with incorrect credentials correctly rejected.")

        print("PASS: test_register_and_login passed.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
