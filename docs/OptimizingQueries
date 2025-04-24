# Check and Optimize Database Queries for Performance Improvements.

This document outlines the tasks completed during sprint 5 to optimize the performance of the inventory management system. The focus was on improving database query performance, ensuring scalability, and verifying the changes through testing.

## 1. Analyze Current Database Queries Using Profiling Tools

To identify inefficient queries, I first compiled a list of all the queries used in the application. 

### SQL Queries in `app.py`

| Function / Route              | SQL Query                                                                                   | Purpose                           |
|------------------------------|----------------------------------------------------------------------------------------------|-----------------------------------|
| `sell_item()`                | `SELECT stock, name, quality FROM inventory WHERE sku = ?`                                  | Check stock                       |
|                              | `UPDATE inventory SET stock = ? WHERE sku = ?`                                              | Update inventory                  |
|                              | `INSERT INTO sales (sku, name, quality, quantity, sale_price) VALUES (?, ?, ?, ?, ?)`      | Record sale                       |
| `sales_page()`               | `SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = ?` | Calculate current month revenue  |
|                              | `SELECT sales.sku, COALESCE(...), ... FROM sales LEFT JOIN inventory ON ... GROUP BY ...`  | Fetch sales details               |
| `api/previous_month_sales`   | `SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = ?` | Previous month revenue           |
|                              | `SELECT sales.sku, sales.name, ... FROM sales WHERE ... GROUP BY ...`                       | Previous month detailed sales     |
| `inventory_data()`           | `SELECT * FROM inventory`                                                                   | Get inventory                     |
| `admin_page()`               | `SELECT id, employee_id, first_name, last_name, role FROM users`                            | Admin user listing                |
| `delete_user_route(user_id)` | `SELECT * FROM users WHERE id = ?`                                                          | Check user exists                 |
|                              | `DELETE FROM users WHERE id = ?`                                                            | Delete user                       |
| `inventory_sort()`           | `SELECT * FROM inventory ORDER BY {sort_by} {order}`                                        | Sorted inventory                  |
| `add_inventory()`            | `SELECT * FROM inventory WHERE sku = ?`                                                     | Check duplicate SKU               |
|                              | `INSERT INTO inventory (...) VALUES (?, ?, ?, ?, ?, ?, ?)`                                  | Add item                          |
| `delete_inventory()`         | `DELETE FROM inventory WHERE sku = ?`                                                       | Delete item                       |
| `api_total_revenue()`        | `SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = ?` | Return current revenue via API   |
| `update_inventory()`         | `SELECT * FROM inventory WHERE sku = ?`                                                     | Check item exists                 |
|                              | `UPDATE inventory SET sku = ?, name = ?, ... WHERE sku = ?`                                 | Update item                       |
| `get_latest_sku()`           | `SELECT sku FROM inventory ORDER BY sku DESC LIMIT 1`                                       | Get latest SKU                    |
| `get_item_by_id(item_id)`    | `SELECT * FROM inventory WHERE sku = ?`                                                     | Get item details                  |

### SQL Queries in `db_setup.py`

| Function   | SQL Query                                                                 |
|------------|---------------------------------------------------------------------------|
| `init_db()`| `CREATE TABLE IF NOT EXISTS inventory (...)` — Creates inventory table    |
|            | `CREATE TABLE IF NOT EXISTS sales (...)` — Creates sales table            |

### SQL Queries in `login.py`

| Function                        | SQL Query                                                                 |
|----------------------------------|---------------------------------------------------------------------------|
| `get_user_by_employee_id()`     | `SELECT * FROM users WHERE employee_id = ?`                               |
| `create_user()`                 | `INSERT INTO users (...) VALUES (?, ?, ?, ?, ?)`                         |
| `setup_database()`              | `CREATE TABLE IF NOT EXISTS users (...)`                                  |


I then utilized profiling tools like `EXPLAIN` and query logs to analyze the performance of these queries. This allowed me to pinpoint slow-performing queries. I created a test script to run these queries on SQLOnline and reviewed the profiling results to identify areas for optimization.

```
-- Create inventory table
CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    original_packaging BOOLEAN NOT NULL,
    quality TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL DEFAULT 0.0
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    name TEXT,
    quality TEXT,
    quantity INTEGER NOT NULL,
    sale_price REAL NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku) REFERENCES inventory(sku)
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Insert sample data into inventory
INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock, price)
VALUES 
('ABC123', 'Product A', 'Platform X', 1, 'New', 100, 25.99),
('DEF456', 'Product B', 'Platform Y', 1, 'Used', 50, 15.49),
('GHI789', 'Product C', 'Platform Z', 0, 'Refurbished', 75, 45.00);

-- Insert sample data into sales
INSERT INTO sales (sku, name, quality, quantity, sale_price)
VALUES
('ABC123', 'Product A', 'New', 2, 25.99),
('DEF456', 'Product B', 'Used', 1, 15.49),
('ABC123', 'Product A', 'New', 3, 25.99);

-- Insert sample data into users
INSERT INTO users (employee_id, first_name, last_name, role, password)
VALUES
('E001', 'John', 'Doe', 'Admin', 'password123'),
('E002', 'Jane', 'Smith', 'Manager', 'password456');

-- EXPLAIN for queries in app.py

-- Check stock
EXPLAIN QUERY PLAN SELECT stock, name, quality FROM inventory WHERE sku = 'ABC123';

-- Update inventory
EXPLAIN QUERY PLAN UPDATE inventory SET stock = 120 WHERE sku = 'ABC123';

-- Record sale
EXPLAIN QUERY PLAN INSERT INTO sales (sku, name, quality, quantity, sale_price) VALUES ('DEF456', 'Product B', 'Used', 2, 15.49);

-- Calculate current month revenue
EXPLAIN QUERY PLAN SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = '2025-04';

-- Fetch sales details
EXPLAIN QUERY PLAN SELECT sales.sku, sales.name, sales.quantity, sales.sale_price, inventory.name AS inventory_name 
FROM sales 
LEFT JOIN inventory ON sales.sku = inventory.sku 
GROUP BY sales.sku;

-- Previous month revenue
EXPLAIN QUERY PLAN SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = '2025-03';

-- Previous month detailed sales
EXPLAIN QUERY PLAN SELECT sales.sku, sales.name, sales.quantity, sales.sale_price FROM sales WHERE strftime('%Y-%m', sale_date) = '2025-03';

-- Get inventory
EXPLAIN QUERY PLAN SELECT * FROM inventory;

-- Admin user listing
EXPLAIN QUERY PLAN SELECT id, employee_id, first_name, last_name, role FROM users;

-- Check user exists
EXPLAIN QUERY PLAN SELECT * FROM users WHERE id = 1;

-- Delete user
EXPLAIN QUERY PLAN DELETE FROM users WHERE id = 1;

-- Sorted inventory
EXPLAIN QUERY PLAN SELECT * FROM inventory ORDER BY name ASC;

-- Check duplicate SKU
EXPLAIN QUERY PLAN SELECT * FROM inventory WHERE sku = 'DEF456';

-- Add item
EXPLAIN QUERY PLAN INSERT INTO inventory (sku, name, platform, original_packaging, quality, stock, price) VALUES ('JKL012', 'Product D', 'Platform X', 1, 'New', 200, 39.99);

-- Delete item
EXPLAIN QUERY PLAN DELETE FROM inventory WHERE sku = 'GHI789';

-- Return current revenue via API
EXPLAIN QUERY PLAN SELECT SUM(quantity * sale_price) as total_revenue FROM sales WHERE strftime('%Y-%m', sale_date) = '2025-04';

-- Check item exists
EXPLAIN QUERY PLAN SELECT * FROM inventory WHERE sku = 'ABC123';

-- Update item
EXPLAIN QUERY PLAN UPDATE inventory SET stock = 150 WHERE sku = 'ABC123';

-- Get latest SKU
EXPLAIN QUERY PLAN SELECT sku FROM inventory ORDER BY sku DESC LIMIT 1;

-- Get item details
EXPLAIN QUERY PLAN SELECT * FROM inventory WHERE sku = 'DEF456';

-- EXPLAIN for queries in db_setup.py

-- Creating inventory table
EXPLAIN QUERY PLAN CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    original_packaging BOOLEAN NOT NULL,
    quality TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL DEFAULT 0.0
);

-- Creating sales table
EXPLAIN QUERY PLAN CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    name TEXT,
    quality TEXT,
    quantity INTEGER NOT NULL,
    sale_price REAL NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku) REFERENCES inventory(sku)
);

-- EXPLAIN for queries in login.py

-- Get user by employee ID
EXPLAIN QUERY PLAN SELECT * FROM users WHERE employee_id = 'E001';

-- Create user
EXPLAIN QUERY PLAN INSERT INTO users (employee_id, first_name, last_name, role, password)
VALUES ('E003', 'Sam', 'Johnson', 'Employee', 'password789');

-- Setup users table
EXPLAIN QUERY PLAN CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL,
    password TEXT NOT NULL
);
```

## RESULTS of SQL EXPLAIN TEST SCRIPT

### SEARCH inventory USING INDEX sqlite_autoindex_inventory_1 (sku=?)
Tables involved: inventory

Operation: Index Search

Details: SQLite is using an automatic index on the sku column to search.

✅ This is good — it means it's not scanning the whole table, it's using the PRIMARY KEY or unique constraint index for fast lookups.

This result came from queries like:

```sql
SELECT stock, name, quality FROM inventory WHERE sku = ?
```
AND
```sql
UPDATE inventory SET stock = ? WHERE sku = ?
```


### 🐢 SCAN sales
Tables involved: sales

Operation: Full Table Scan

❌ This could be improved.

This usually happens for queries like:

```sql
SELECT SUM(quantity * sale_price) as total_revenue 
FROM sales 
WHERE strftime('%Y-%m', sale_date) = ?
```
Why it's slow:

SQLite has to go row-by-row because there's no index on sale_date, and the strftime() function makes it hard to optimize.

*No direct code changes were made for this task, but a thorough analysis was done using profiling tools and scripts.*

## 2. Add Missing Indexes and Rewrite Inefficient Queries

To optimize performance, I added the sale_month column in db_setup.py, populated it using strftime, and indexed it. I also rewrote the queries in app.py to use sale_month instead of strftime('%Y-%m', sale_date). I edited the changes in db_setup.py and app.py

## 3. Test the optimized queries in a staging environment
I created and ran a test script using EXPLAIN QUERY PLAN on the  inventory.db to confirm the optimizations. The test script is included in its own file.

## 4. Ensure database can take and load information at a constant speed without slowing
The stress/load tests that were created earlier in the sprints test this feature
