import unittest
import sqlite3
import db_setup  # Import your db_setup module

class TestInventoryDatabase(unittest.TestCase):
    def setUp(self):
        # Use a shared in-memory SQLite database URI.
        self.db_uri = "file:memdb1?mode=memory&cache=shared"
        # Open a persistent connection to keep the shared DB alive.
        self.persistent_connection = sqlite3.connect(self.db_uri, uri=True)
        self.persistent_connection.row_factory = sqlite3.Row

        # Helper function to create a new connection with row_factory set.
        def create_connection():
            conn = sqlite3.connect(self.db_uri, uri=True)
            conn.row_factory = sqlite3.Row
            return conn

        # Monkey-patch get_db_connection to always return a new connection to our shared DB.
        self.original_get_db_connection = db_setup.get_db_connection
        db_setup.get_db_connection = lambda: create_connection()

        # Initialize the database schema.
        db_setup.init_db()

    def tearDown(self):
        # Restore the original get_db_connection function.
        db_setup.get_db_connection = self.original_get_db_connection
        # Close the persistent connection.
        self.persistent_connection.close()

    def test_insert_and_retrieve_item(self):
        print("Running test_insert_and_retrieve_item: Testing insertion and retrieval of item.")
        # Insert a test item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        sku = "1231-0G"
        cursor.execute(
            "INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (sku, "Test Game", "Xbox", 1, "Good", 10)
        )
        conn.commit()
        conn.close()

        # Retrieve the item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
        item = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Test Game")
        print("PASS: test_insert_and_retrieve_item passed.")

    def test_update_stock(self):
        print("Running test_update_stock: Testing update of stock quantity.")
        # Insert a test item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        sku = "1231-0G"
        cursor.execute(
            "INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (sku, "Test Game", "Xbox", 1, "Good", 10)
        )
        conn.commit()
        conn.close()

        # Update the stock value.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET stock = ? WHERE sku = ?", (20, sku))
        conn.commit()
        conn.close()

        # Retrieve and check updated stock.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM inventory WHERE sku = ?", (sku,))
        item = cursor.fetchone()
        conn.close()
        self.assertEqual(item["stock"], 20)
        print("PASS: test_update_stock passed.")

    def test_delete_item(self):
        print("Running test_delete_item: Testing deletion of an item.")
        # Insert a test item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        sku = "1231-0G"
        cursor.execute(
            "INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock) VALUES (?, ?, ?, ?, ?, ?)",
            (sku, "Test Game", "Xbox", 1, "Good", 10)
        )
        conn.commit()
        conn.close()

        # Delete the item.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE sku = ?", (sku,))
        conn.commit()
        conn.close()

        # Verify deletion.
        conn = db_setup.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
        item = cursor.fetchone()
        conn.close()
        self.assertIsNone(item)
        print("PASS: test_delete_item passed.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
