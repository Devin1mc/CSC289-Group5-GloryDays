import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database and insert sample data if needed
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create inventory table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        sku TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT NOT NULL,
        original_packaging BOOLEAN NOT NULL,
        quality TEXT NOT NULL,
        stock INTEGER NOT NULL,
        price REAL NOT NULL DEFAULT 0.0  -- Added price column with default value 0.0
    )
    ''')

    # Create the sales table for tracking sales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            name TEXT,
            quality TEXT,
            quantity INTEGER NOT NULL,
            sale_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sku) REFERENCES inventory(sku)
        )
    ''')

    # add sale_month column if it's not already there
    cursor.execute("PRAGMA table_info(sales)")
    columns = [row["name"] for row in cursor.fetchall()]
    if "sale_month" not in columns:
        cursor.execute("ALTER TABLE sales ADD COLUMN sale_month TEXT")

    # fill in sale_month for existing sales
    cursor.execute("""
        UPDATE sales
        SET sale_month = strftime('%Y-%m', sale_date)
        WHERE sale_month IS NULL
    """)

    # add index on sale_month to make queries faster
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_sale_month ON sales(sale_month)")

    conn.commit()
    conn.close()
