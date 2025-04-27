import unittest
import sqlite3
import re
from flask import Flask, session
import sys
import os

current_dir = os.path.dirname(__file__)  # test_files/
src_dir = os.path.abspath(os.path.join(current_dir, '..'))  # Go up to src/
sys.path.append(src_dir)

from login import auth_bp, setup_database


class TestSecurity(unittest.TestCase):
    # This method runs before every test
    def setUp(self):
        # Create a test Flask app and register login routes
        self.app = Flask(__name__)
        self.app.secret_key = 'test'
        self.app.register_blueprint(auth_bp)
        self.client = self.app.test_client()

        # Ensure the database is initialized
        with self.app.app_context():
            setup_database()

    def test_inventory_data_no_login(self):
        print("\n🔒 TEST: Attempting to access /inventory without logging in.")
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 302)
        print("✅ PASS: Unauthenticated user was correctly redirected (status code 302).")

    def test_passwords_are_hashed(self):
        print("\n🔐 TEST: Checking that all passwords in the database are hashed with SHA-256 format.")
        # Path to the database where user credentials are stored
        db_path = "login_database.db"
        conn = sqlite3.connect(db_path) # Connect to the SQLite database
        cursor = conn.cursor()

        # Retrieve all stored password hashes from the users table
        cursor.execute("SELECT password_hash FROM users")
        passwords = cursor.fetchall()
        conn.close() # Close the connection to the database

        hash_pattern = re.compile(r'^[a-fA-F0-9]{64}$')  # SHA-256 is 64-character hex

        # Loop through all password hashes and check if they match the SHA-256 format
        for idx, (password_hash,) in enumerate(passwords, 1):
            self.assertRegex(
                password_hash,
                hash_pattern,
                msg=f"❌ FAIL: Entry {idx} does not appear to be a properly hashed password: {password_hash}"
            )
            print(f"✅ PASS: Entry {idx} is hashed correctly.")

if __name__ == "__main__":
    unittest.main()
