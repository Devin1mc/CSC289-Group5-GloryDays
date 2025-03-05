from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from login import auth_bp, setup_database, get_user_connection
import sqlite3
from db_setup import get_db_connection, init_db

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
    cursor.execute("SELECT stock FROM inventory WHERE sku = ?", (sku,))
    item = cursor.fetchone()
    if not item:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    current_stock = item['stock']
    if current_stock < quantity:
        conn.close()
        return jsonify({"error": "Insufficient stock"}), 400

    # Deduct the quantity and record the sale
    new_stock = current_stock - quantity
    cursor.execute("UPDATE inventory SET stock = ? WHERE sku = ?", (new_stock, sku))
    cursor.execute("INSERT INTO sales (sku, quantity, sale_price) VALUES (?, ?, ?)", (sku, quantity, sale_price))
    conn.commit()
    conn.close()

    return jsonify({"message": "Sale successful", "new_stock": new_stock})

@app.route('/sales')
def sales_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            sales.sku, 
            date(sales.sale_date) as sale_date,
            inventory.quality as condition,
            SUM(sales.quantity) as total_quantity,
            AVG(sales.sale_price) as avg_sale_price
        FROM sales
        JOIN inventory ON sales.sku = inventory.sku
        GROUP BY sales.sku, date(sales.sale_date), inventory.quality
        ORDER BY sale_date DESC
    """)
    sales = cursor.fetchall()
    conn.close()
    return render_template("sales.html", sales=sales)

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
        return redirect(url_for('auth_bp.login'))  # Redirect to the login page if not logged in or not an admin

    # Fetch the list of users and their roles from the database
    user_conn = get_user_connection()
    cursor = user_conn.cursor()
    cursor.execute("SELECT id, employee_id, first_name, last_name, role FROM users")
    users = cursor.fetchall()
    user_conn.close()

    # Pass the list of users to the admin template
    return render_template('admin.html', users=users)


@app.route('/inventory')
def inventory_page():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    conn.close()

    # Convert SQLite Row objects to dictionaries for easier access in templates
    inventory_list = [dict(item) for item in inventory]
    
    # Return the inventory data as JSON
    return jsonify(inventory_list)

@app.route('/remove_user/<int:user_id>', methods=['POST'])
def delete_user_route(user_id):
    # Check if the current user is logged in and is an admin
    if 'user' not in session or session.get('role') != 'admin':
        flash("You don't have permission to perform this action.", 'danger')
        return redirect(url_for('admin_page'))  # Redirect back to the admin page if not an admin

    # Deleting the user from the database
    try:
        user_conn = get_db_connection()
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


if __name__ == "__main__":
    app.run(debug=True)