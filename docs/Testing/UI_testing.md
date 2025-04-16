# UI Test Project Documentation

## Overview

This document details the automation UI test developed using Selenium WebDriver for verifying functionality of an inventory management web application. The test script validates essential features such as logging in, managing inventory items (addition and deletion), and logging out.

## Tools and Technologies

- **Selenium WebDriver** (Python bindings)
- **ChromeDriver** (for Google Chrome automation)
- **WebDriverWait and Expected Conditions (EC)** (for handling dynamic web elements)
- **Python** (Scripting Language)

## Testing Procedure

### Step 1: User Login Verification

- **Navigate to the Login Page:** The test begins by navigating to the login page at `http://localhost:5000/`.
- **Input Credentials:** 
  - Username (`employee_id`): Entered as "user".
  - Password: Entered as "pass".
- **Submit Credentials:** Credentials submitted by triggering the RETURN key event on the password field.
- **Validation:** Ensures successful login by checking the presence of text "Employee:" on the inventory page.

### Step 2: Adding an Inventory Item

- **Triggering Modal:** Clicks the "Add Item" button, expecting the modal (`addItemModal`) to appear.
- **Filling Out Item Details:**
  - SKU: `TESTSKU`
  - Name: `Test Game`
  - Platform: `PC`
  - Original Packaging: Checked
  - Quality: `Good`
  - Stock: `10`
- **Submission:** Submits form and handles the subsequent alert, confirming whether the item was successfully added or already exists.
- **Modal Handling:** If the item already exists, closes the modal to maintain test continuity.
- **Inventory Check:** Confirms the presence of the newly added item or its prior existence by scanning the inventory list.

### Step 3: Deleting an Inventory Item

- **Item Deletion:** Finds the delete button for the specific item (`TESTSKU`) and triggers deletion.
- **Prompt Handling:**
  - JavaScript prompt appears, confirming deletion with the text "Delete".
  - Subsequent confirmation alert is also handled.
- **Post-deletion Verification:** Verifies removal of the item from the inventory list.

### Step 4: User Logout Verification

- **Logout Process:** Clicks the "Logout" button.
- **Redirection Check:** Confirms successful logout by ensuring the presence of login elements (`employee_id`) on the redirected login page.

## Error Handling and Alerts

- **Item Addition:** Handles alerts indicating item pre-existence gracefully by ensuring modal closure.
- **Deletion Prompts:** Manages JavaScript confirmation prompts and alerts effectively, ensuring accurate test execution.

## Test Completion

- Closes and quits the Chrome WebDriver instance upon test completion or unexpected termination.

## Outcomes and Validation

- Each action step includes a validation check to ensure the UI reflects expected behavior (successful login, item presence, successful deletion, and logout).
- Informative console logs are printed throughout the test to indicate progress and results, supporting debugging and verification.

## Conclusion

The automated UI test script effectively verifies the core functionalities of user authentication, inventory item management, and session handling. Continuous execution of this script aids in early detection of UI issues, ensuring robust software quality.