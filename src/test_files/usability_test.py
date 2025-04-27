import unittest
import os
import sqlite3
import hashlib
import sys

# Add src/ to sys.path
current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(src_dir)

# Import necessary modules from the source code
# These is one folder up from test_files
from login import setup_database
from app import app
import db_setup

############################################
# Employee Database Tests
############################################

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
        
        # Ensure a clean state by dropping the users table if it exists.
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()
        conn.close()
        
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
        print("=== Employee DB Testing ===")
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

        print("PASS: Employee DB tests passed.\n")

############################################
# Inventory Database Tests
############################################

class TestInventoryDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary inventory database file.
        self.test_inventory_db = "test_inventory.db"
        if os.path.exists(self.test_inventory_db):
            os.remove(self.test_inventory_db)
        
        # Monkey-patch db_setup.get_db_connection to use our test inventory database.
        self.original_get_db_connection = db_setup.get_db_connection
        db_setup.get_db_connection = lambda: self.create_test_inventory_connection()
        
        # Initialize the inventory database schema.
        db_setup.init_db()

    def create_test_inventory_connection(self):
        conn = sqlite3.connect(self.test_inventory_db)
        conn.row_factory = sqlite3.Row
        return conn

    def tearDown(self):
        # Restore the original get_db_connection.
        db_setup.get_db_connection = self.original_get_db_connection
        if os.path.exists(self.test_inventory_db):
            os.remove(self.test_inventory_db)

    def test_inventory_operations(self):
        print("=== Inventory DB Testing ===")
        # Insert a test inventory item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        sku = "SKU001"
        item_name = "Test Game"
        platform = "Xbox"
        original_packaging = 1  # Using 1 for True
        quality = "Good"
        stock = 10
        price = 59.99
        cursor.execute(
            "INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock, price) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (sku, item_name, platform, original_packaging, quality, stock, price)
        )
        conn.commit()
        conn.close()
        print("Inserted inventory item:", sku)

        # Retrieve the inserted item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
        item = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], item_name)
        print("Retrieved inventory item:", dict(item))

        # Update the stock value.
        new_stock = 20
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET stock = ? WHERE sku = ?", (new_stock, sku))
        conn.commit()
        conn.close()
        print("Updated stock for", sku, "to", new_stock)

        # Verify the stock update.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM inventory WHERE sku = ?", (sku,))
        updated_item = cursor.fetchone()
        conn.close()
        self.assertEqual(updated_item["stock"], new_stock)
        print("Verified updated stock for", sku)

        # Delete the item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE sku = ?", (sku,))
        conn.commit()
        conn.close()
        print("Deleted inventory item:", sku)

        # Verify deletion.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
        deleted_item = cursor.fetchone()
        conn.close()
        self.assertIsNone(deleted_item)
        print("Verified deletion for", sku)
        print("PASS: Inventory DB tests passed.\n")

if __name__ == "__main__":
    unittest.main(verbosity=2)
