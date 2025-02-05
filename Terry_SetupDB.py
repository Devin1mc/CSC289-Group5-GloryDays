"""
Filename: Terry_SetupDB.py
Date: February 4, 2025
Programmer: Terry Wiggins
Purpose: This program provides a command-line interface (CLI) for managing an inventory of video games using an SQLite database.
It allows users to add new items, retrieve item details by SKU, update stock levels, delete inventory items, and list all stored items.
The system automatically generates SKUs in the format XXXY-ZK, where:
  - XXX: Base item ID
  - Y: Platform (1 = Xbox, 2 = PlayStation, 3 = PC)
  - Z: Packaging (0 = No packaging, 1 = With original packaging)
  - K: Quality (G = Good, L = Like New, O = Old)
"""

import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        sku TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT NOT NULL,
        original_packaging BOOLEAN NOT NULL,
        quality TEXT NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# SKU Generation
def generate_sku(base_id, platform, packaging, quality):
    return f"{base_id}{platform}-{packaging}{quality}"

# Mappings
platform_map = {"1": "Xbox", "2": "PlayStation", "3": "PC", "4": "Other"}
quality_map = {"G": "Good", "L": "Like New", "O": "Old"}

# List Base Item IDs
def list_base_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT SUBSTR(sku, 1, 3) AS base_id, name FROM inventory ORDER BY base_id")
    items = cursor.fetchall()
    conn.close()

    if items:
        print("\nAvailable Base Item IDs:")
        for item in items:
            print(f"Base ID: {item['base_id']} - Game: {item['name']}")
        print()
    else:
        print("No games found in inventory. Add a new game with a unique ID.")


# Add item function with Base ID validation
def add_item():
    # Show existing Base Item IDs before adding a new item
    list_base_ids()

    base_id = input("Enter base item ID (or assign a new one): ")

    # Check if the base ID is already in use
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM inventory WHERE SUBSTR(sku, 1, 3) = ?", (base_id,))
    existing_game = cursor.fetchone()

    if existing_game:
        print(f"Error: Base ID {base_id} is already assigned to '{existing_game['name']}'")
        print("If this is the same game, please proceed with the correct name.")
        print("Otherwise, assign a new Base ID for the new game.")
        conn.close()
        return

    name = input("Enter game name: ")
    platform = input("Enter platform (1: Xbox, 2: PlayStation, 3: PC, 4: Other): ")
    packaging = input("Enter packaging (0: No, 1: Yes): ")
    quality = input("Enter quality (G: Good, L: Like New, O: Old): ").upper()
    stock = input("Enter stock quantity: ")

    if platform not in platform_map or quality not in quality_map or packaging not in ["0", "1"]:
        print("Invalid input. Try again.")
        conn.close()
        return

    sku = generate_sku(base_id, platform, packaging, quality)

    cursor.execute(
        "INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock) VALUES (?, ?, ?, ?, ?, ?)",
        (sku, name, platform_map[platform], int(packaging), quality_map[quality], stock))
    conn.commit()
    conn.close()
    print(f"Item added with SKU: {sku}")


# This function will retrieve item by SKU
def get_item():
    sku = input("Enter SKU to retrieve: ").upper() # Convert the input to uppercase
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
    item = cursor.fetchone()
    conn.close()

    if item:
        print(f"\nSKU: {item['sku']}, Name: {item['name']}, Platform: {item['platform']}, "
              f"Packaging: {'Yes' if item['original_packaging'] else 'No'}, Quality: {item['quality']}, Stock: {item['stock']}\n")
    else:
        print("Item not found.")

# This function will update stock
def update_stock():
    sku = input("Enter SKU to update: ")
    new_stock = input("Enter new stock quantity: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET stock = ? WHERE sku = ?", (new_stock, sku))
    conn.commit()
    conn.close()
    print(f"Stock updated for SKU {sku}.")

# This function will delete item
def delete_item():
    sku = input("Enter SKU to delete: ")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE sku = ?", (sku,))
    conn.commit()
    conn.close()
    print(f"Item with SKU {sku} deleted.")

# This function will list all items
def list_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()

    if items:
        print("\nGlory Days Inventory List:")
        for item in items:
            print(f"SKU: {item['sku']}, Name: {item['name']}, Platform: {item['platform']}, "
                  f"Packaging: {'Yes' if item['original_packaging'] else 'No'}, Quality: {item['quality']}, Stock: {item['stock']}")
        print()
    else:
        print("No inventory found.")

# CLI menu
def main():
    init_db()
    while True:
        print("\nGlory Days Inventory System")
        print("1. Add New Item")
        print("2. Get Item by SKU")
        print("3. Update Stock")
        print("4. Delete Item")
        print("5. List Inventory")
        print("6. List Base Item IDs")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            get_item()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            list_inventory()
        elif choice == "6":
            list_base_ids()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
