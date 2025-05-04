# Database Schemas

## 1. `login_database.db`

This database stores employee login information securely, including password hashes and user roles.

### Table: `users`

| Column         | Type     | Description                                | Constraints                     |
|----------------|----------|--------------------------------------------|---------------------------------|
| id             | INTEGER  | Unique ID for each user                   | Primary Key, Auto-increment     |
| first_name     | TEXT     | Employee's first name                      | Not Null                        |
| last_name      | TEXT     | Employee's last name                       | Not Null                        |
| employee_id    | TEXT     | Unique employee identifier                 | Unique, Not Null                |
| role           | TEXT     | User role (default is 'user')               | Default = 'user'                |
| password_hash  | TEXT     | Hashed password                            | Not Null                        |

---

## 2. `inventory.db`

This database manages the store's inventory and records sales transactions.

### Table: `inventory`

| Column             | Type    | Description                                     | Constraints            |
|--------------------|---------|-------------------------------------------------|-------------------------|
| sku                | TEXT    | Unique product identifier (SKU)                | Primary Key             |
| name               | TEXT    | Name of the product                            | Not Null                |
| platform           | TEXT    | Platform (e.g., PS5, Xbox, etc.)                | Not Null                |
| original_packaging | BOOLEAN | Whether the product has its original packaging | Not Null                |
| quality            | TEXT    | Condition/quality rating of the product        | Not Null                |
| stock              | INTEGER | Number of items in stock                       | Not Null                |
| price              | REAL    | Price of the product                           | Default = 0.0           |

### Table: `sales`

| Column       | Type      | Description                                  | Constraints                        |
|--------------|-----------|----------------------------------------------|------------------------------------|
| sale_id      | INTEGER   | Unique sale transaction ID                   | Primary Key, Auto-increment        |
| sku          | TEXT      | SKU of the item sold                         | Foreign Key → `inventory.sku`      |
| quantity     | INTEGER   | Quantity of the item sold                    | Not Null                           |
| sale_price   | REAL      | Price at which the item was sold             | Not Null                           |
| sale_date    | TIMESTAMP | Timestamp when the sale occurred             | Default = CURRENT_TIMESTAMP        |
| name         | TEXT      | Name of the product sold (copied at sale time)| Optional                           |
| quality      | TEXT      | Quality of the product sold (copied at sale time)| Optional                        |

---

## Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        INTEGER id PK "Primary Key"
        TEXT first_name "Employee's First Name"
        TEXT last_name "Employee's Last Name"
        TEXT employee_id "Unique Employee ID"
        TEXT role "User Role (default 'user')"
        TEXT password_hash "Hashed Password"
    }

    INVENTORY {
        TEXT sku PK "Product SKU (Primary Key)"
        TEXT name "Product Name"
        TEXT platform "Platform (e.g., PS5, Xbox)"
        BOOLEAN original_packaging "Original Packaging (true/false)"
        TEXT quality "Quality of the Product"
        INTEGER stock "Quantity in Stock"
        REAL price "Price of the Product"
    }

    SALES {
        INTEGER sale_id PK "Sale ID (Primary Key)"
        TEXT sku FK "SKU of the Sold Item"
        INTEGER quantity "Quantity Sold"
        REAL sale_price "Price at Sale Time"
        TIMESTAMP sale_date "Date of Sale"
        TEXT name "Name of Product at Time of Sale"
        TEXT quality "Quality at Time of Sale"
    }

    INVENTORY ||--o{ SALES : "sku"
