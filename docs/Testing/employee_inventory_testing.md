# Test Documentation for Employee and Inventory Database Tests

## Overview

This document describes the automated tests used to verify the employee and inventory database functionalities for the Glory Days application. The tests are implemented using Python’s `unittest` framework and are divided into two main parts:

- **Employee Database Tests:** Validate user registration and login workflows.
- **Inventory Database Tests:** Verify CRUD (Create, Read, Update, Delete) operations on the inventory table.

---

## Files

- **test_employee.py:**  
  Contains tests for the employee database functions, including:
  - Registration with valid admin credentials.
  - Login using correct credentials.
  - Login failure with incorrect credentials.

- **test_inventory.py:**  
  Contains tests for the inventory database functions, including:
  - Inserting an inventory item and retrieving it.
  - Updating the stock value of an item.
  - Deleting an item and verifying its removal.

---

## Prerequisites

- Python 3.x installed.
- SQLite3 available (using Python’s built-in `sqlite3` module).
- Required modules: `login.py`, `app.py`, and `db_setup.py` must be located in the source directory.

---

## Running the Tests

### Employee Test

Run the following command to execute the employee tests:

```bash
python test_employee.py
```
Employee Database Tests
Purpose

These tests ensure that:

    A new employee can register when valid admin credentials are provided.

    A registered employee can log in with correct credentials.

    Login attempts with an incorrect password are properly rejected.

Test Flow
Setup:

    A temporary database file (test_login_database.db) is created.

    The users table is initialized with the correct schema (including the role column) by calling setup_database().

    An admin user is inserted to allow registration.

Registration Test:

    A simulated POST request is sent to the /register endpoint with new employee data along with valid admin credentials.

    The response is checked for a successful registration status.

Valid Login Test:

    A POST request is sent to the /login endpoint with correct credentials.

    The test verifies that the response includes the registered employee's first name.

Invalid Login Test:

    A POST request is sent with an incorrect password.

    The response is checked for an error message indicating "Invalid Employee ID or Password."

### Inventory Test
Run the following command to execute the inventory tests:
``` bash
python test_inventory.py
```
Purpose

These tests verify that the inventory database operations work as expected:

    Insertion and Retrieval: An inventory item can be added and then retrieved correctly.

    Stock Update: Updating the stock value of an item works as intended.

    Deletion: An inventory item can be deleted, and its removal is confirmed.

Test Flow
Setup:

    A shared in-memory SQLite database is used for testing, ensuring a clean environment.

    The init_db() function is called to initialize the inventory schema.

Insertion and Retrieval Test:

    A test item is inserted into the inventory table.

    The item is retrieved by its SKU, and its details (such as name) are verified.

Update Test:

    The stock value of the inserted item is updated.

    The item is retrieved again to verify that the stock value matches the expected new value.

Deletion Test:

    The test item is deleted from the database.

    A subsequent query confirms the item is no longer present.

## Conclusion
These tests provide essential automated verification for critical database functionalities within the Glory Days application. By ensuring that both employee operations (registration and login) and inventory operations (insertion, update, deletion) function correctly, the tests help maintain a robust and reliable system. For further modifications or debugging, refer to the underlying source modules (login.py, db_setup.py, and app.py).