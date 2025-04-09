from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from login import auth_bp, setup_database, get_user_connection
import sqlite3
from db_setup import get_db_connection, init_db
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Register the authentication blueprint from login.py
app.register_blueprint(auth_bp)

# Set up the login database and initialize the inventory and sales tables on startup
setup_database()
init_db()

@app.route('/sell', methods=['POST'])
def sell_item():
    data = request.get_json()
    sku = data.get('sku')
    quantity = int(data.get('quantity', 1))
    sale_price = float(data.get('sale_price', 0))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the item exists and get its current stock
    cursor.execute("SELECT stock, name, quality FROM inventory WHERE sku = ?", (sku,))
    item = cursor.fetchone()

    if not item:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    current_stock = item["stock"]
    if current_stock < quantity:
        conn.close()
        return jsonify({"error": "Insufficient stock"}), 400

    # Deduct the quantity and record the sale
    new_stock = current_stock - quantity
    cursor.execute("UPDATE inventory SET stock = ? WHERE sku = ?", (new_stock, sku))
    cursor.execute(
    "INSERT INTO sales (sku, name, quality, quantity, sale_price) VALUES (?, ?, ?, ?, ?)",
    (sku, item["name"], item["quality"], quantity, sale_price)
)

    conn.commit()
    conn.close()

    return jsonify({"message": "Sale successful", "new_stock": new_stock})

@app.route('/sales')
def sales_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get current month in YYYY-MM format
    current_month = datetime.now().strftime('%Y-%m')
    
    # Calculate total revenue for the current month
    cursor.execute("""
        SELECT SUM(quantity * sale_price) as total_revenue 
        FROM sales 
        WHERE strftime('%Y-%m', sale_date) = ?
    """, (current_month,))
    result = cursor.fetchone()
    total_revenue = result["total_revenue"] if result["total_revenue"] is not None else 0.0

    # Updated sales records query to ensure all sales are displayed, even if they are not in inventory
    cursor.execute("""
        SELECT 
            sales.sku,
            COALESCE(inventory.name, sales.name, 'Unlisted Item') AS item_name,
            sales.sale_date AS sale_date,
            COALESCE(inventory.quality, sales.quality, 'Unknown') AS condition,
            SUM(sales.quantity) AS total_quantity,
            SUM(sales.quantity * sales.sale_price) AS total_sales_value
        FROM sales
        LEFT JOIN inventory ON sales.sku = inventory.sku
        WHERE strftime('%Y-%m', sales.sale_date) = ?
        GROUP BY sales.sku, sales.sale_date, condition
        ORDER BY sale_date DESC
    """, (current_month,))
    sales = cursor.fetchall()
    conn.close()
    
    # Pass total_revenue and sales records to the template
    return render_template("sales.html", sales=sales, total_revenue=total_revenue)

# Endpoint to return previous month sales data
@app.route('/api/previous_month_sales')
def api_previous_month_sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate the previous month in YYYY-MM format
    first_day_this_month = datetime.today().replace(day=1)
    last_month = first_day_this_month - timedelta(days=1)
    prev_month_str = last_month.strftime('%Y-%m')

    # Calculate total revenue for previous month
    cursor.execute("""
        SELECT SUM(quantity * sale_price) as total_revenue 
        FROM sales 
        WHERE strftime('%Y-%m', sale_date) = ?
    """, (prev_month_str,))
    result = cursor.fetchone()
    total_revenue = result["total_revenue"] if result["total_revenue"] is not None else 0.0

        # Get detailed previous month sales grouped by SKU, date, and quality
    cursor.execute("""
        SELECT 
            sales.sku,
            sales.name AS item_name,
            DATE(sales.sale_date) AS sale_date,
            sales.quality AS condition,
            SUM(sales.quantity) AS total_quantity,
            SUM(sales.quantity * sales.sale_price) AS total_sales_value
        FROM sales
        WHERE strftime('%Y-%m', sales.sale_date) = ?
        GROUP BY sales.sku, DATE(sales.sale_date), sales.quality
        ORDER BY sale_date DESC
        """, (prev_month_str,))


    sales_details = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify({"total_revenue": total_revenue, "sales_details": sales_details})

@app.route('/inventory_data')
def inventory_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    # Convert SQLite Row objects to dictionaries
    items_list = [dict(item) for item in items]
    return jsonify(items_list)

@app.route('/admin')
def admin_page():
    # Check if the user is logged in and has an admin role
    if 'user' not in session or session.get('role') != 'admin':
        flash("You don't have permission to view this page.", 'danger')
        return redirect(url_for('auth.login_page'))  # Correct Blueprint route

    # Fetch the list of users and their roles from the database
    user_conn = get_user_connection()
    cursor = user_conn.cursor()
    cursor.execute("SELECT id, employee_id, first_name, last_name, role FROM users")
    users = cursor.fetchall()
    user_conn.close()

    # Pass the list of users to the admin template
    return render_template('admin.html', users=users)

@app.route('/remove_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    # Check if the current user is logged in and is an admin
    if 'user' not in session or session.get('role') != 'admin':
        flash("You don't have permission to perform this action.", 'danger')
        return redirect(url_for('admin_page'))  # Redirect back to the admin page if not an admin

    # Deleting the user from the database
    try:
        user_conn = get_user_connection()
        cursor = user_conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash("User not found.", 'danger')
            return redirect(url_for('admin_page'))  # Redirect back if user not found

        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        user_conn.commit()
        user_conn.close()

        flash('User successfully removed.', 'success')
    except Exception as e:
        flash(f"Error occurred: {e}", 'danger')

    return redirect(url_for('admin_page'))  # Redirect back to the admin page

@app.route('/inventory_data/sort', methods=['GET'])
def inventory_sort():
    # Get sorting parameters from request
    sort_by = request.args.get('sort_by', 'name')  
    order = request.args.get('order', 'asc')  
    order = 'ASC' if order == 'asc' else 'DESC'

    # Define valid columns that can be used for sorting
    valid_sort_columns = ['name', 'sku', 'console', 'condition']
    if sort_by not in valid_sort_columns:
        return jsonify({"error": "Invalid sort parameter"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM inventory ORDER BY {sort_by} {order}")
    items = cursor.fetchall()
    conn.close()

    # Convert SQLite Row objects to dictionaries
    items_list = [dict(item) for item in items]
    return jsonify(items_list)

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    data = request.get_json()
    sku = data.get('sku')
    name = data.get('name')
    platform = data.get('platform')
    original_packaging = data.get('original_packaging', False)
    quality = data.get('quality')
    stock = int(data.get('stock', 0))
    price = float(data.get('price', 0))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the item already exists by SKU
    cursor.execute("SELECT * FROM inventory WHERE sku = ?", (sku,))
    existing_item = cursor.fetchone()
    if existing_item:
        conn.close()
        return jsonify({"error": "Item already exists with the same SKU."}), 400

    # Insert the new item into the inventory
    cursor.execute("""
        INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock, price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (sku, name, platform, original_packaging, quality, stock, price))

    conn.commit()
    conn.close()

    return jsonify({"message": "Item added successfully."})

@app.route('/delete_inventory', methods=['POST'])
def delete_inventory():
    data = request.get_json()
    sku = data.get('sku')

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM inventory WHERE sku = ?", (sku,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item successfully deleted!"})

@app.route('/api/total_revenue')
def api_total_revenue():
    """
    This endpoint returns the total revenue for the current month in JSON format.
    It is intended to be polled by the front-end to automatically update the revenue display.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute("""
        SELECT SUM(quantity * sale_price) as total_revenue 
        FROM sales 
        WHERE strftime('%Y-%m', sale_date) = ?
    """, (current_month,))
    result = cursor.fetchone()
    total_revenue = result["total_revenue"] if result["total_revenue"] is not None else 0.0
    conn.close()
    return jsonify({"total_revenue": total_revenue})

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.get_json()
    original_sku = data.get('original_sku')  # This is the original SKU (before changes)
    sku = data.get('sku')  # New SKU to be saved
    name = data.get('name')
    platform = data.get('platform')
    original_packaging = data.get('original_packaging', False)
    quality = data.get('quality')
    stock = int(data.get('stock', 0))
    price = float(data.get('price', 0))

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the item with the original_sku exists in the database
    cursor.execute("SELECT * FROM inventory WHERE sku = ?", (original_sku,))
    existing_item = cursor.fetchone()

    # If the item doesn't exist, return an error
    if not existing_item:
        conn.close()
        return jsonify({"error": "Item not found."}), 404

    # Update the inventory item with the new SKU and other details
    cursor.execute("""
        UPDATE inventory
        SET sku = ?, name = ?, platform = ?, original_packaging = ?, quality = ?, stock = ?, price = ?
        WHERE sku = ?
    """, (sku, name, platform, original_packaging, quality, stock, price, original_sku))

    conn.commit()
    conn.close()

    return jsonify({"message": "Item updated successfully."})



@app.route('/get_latest_sku', methods=['GET'])
def get_latest_sku():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the highest existing SKU from the database
    cursor.execute("SELECT sku FROM inventory ORDER BY sku DESC LIMIT 1")
    last_item = cursor.fetchone()
    conn.close()

    # Get the latest SKU (if it exists) and extract the first 3 digits
    if last_item:
        latest_sku = last_item['sku']
        latest_item_number = int(latest_sku[:3]) + 1  # Increment the first 3 digits
    else:
        latest_item_number = 1  # Start with 001 if no items exist

    return jsonify({"latest_item_number": str(latest_item_number).zfill(3)})  # Return the next item number as a 3-digit string

@app.route('/get_item_by_id/<item_id>', methods=['GET'])
def get_item_by_id(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the item by SKU (or use item_id if you want to pass the ID instead of SKU)
    cursor.execute('SELECT * FROM inventory WHERE sku = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()

    if item:
        # Return the item details in JSON format
        return jsonify({
            "sku": item['sku'],
            "name": item['name'],
            "platform": item['platform'],
            "original_packaging": item['original_packaging'],
            "quality": item['quality'],
            "stock": item['stock'],
            "price": item['price']
        })
    else:
        return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
