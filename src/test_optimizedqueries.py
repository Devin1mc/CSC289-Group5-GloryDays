import sqlite3

# Connect to the staging database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Run the optimized query
cursor.execute("""
    EXPLAIN QUERY PLAN SELECT SUM(quantity * sale_price) as total_revenue 
    FROM sales WHERE sale_month = '2025-04';
""")
result = cursor.fetchall()
print(result)

# Close the connection
conn.close()
