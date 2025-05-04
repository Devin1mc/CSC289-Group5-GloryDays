# UI Test Project Documentation

## Overview

This document details the automated UI test developed using Selenium WebDriver for verifying the functionality of an inventory management web application. The test script covers user registration, authentication, inventory item management (addition and deletion), and session handling.

This comprehensive UI test script validates critical user flows from user registration through to logout, ensuring every key interaction is thoroughly tested. By incorporating human-like typing simulation, retry logic for modal handling, and robust alert management, the test accurately mimics real-world usage and uncovers potential edge-case failures before they reach production.

The modular structure of the test—breaking down the workflow into discrete steps for registration, login, item addition, deletion, and logout—facilitates easy maintenance and future enhancements. Clear console logging and strategic delays provide transparency into execution flow, speeding up diagnostics in case of test failures. Moreover, the inclusion of backup login credentials enhances resilience, allowing the test to adapt to different test environments without manual intervention.

## Tools and Technologies

- **Python**
- **Selenium WebDriver** (Python bindings)
- **ChromeDriver** (for Google Chrome automation)
- **WebDriverWait and Expected Conditions (EC)** (for handling dynamic web elements)
- **Selenium Common Exceptions** (TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException, ElementClickInterceptedException)
- **time module** (for explicit delays)

## Test Workflow

### Step 0: User Registration

1. **Navigate to the Registration Page**  
   - URL: `http://localhost:5000/register`  
   - Waits for the presence of the `first_name` field.  

2. **Fill Registration Form**  
   - Uses a **slow typing** helper function (`slow_type`) to simulate human typing.  
   - Fields:  
     - `first_name`: "Test"  
     - `last_name`: "User"  
     - `employee_id`: "testuser"  
     - `password`: "password"  
     - `admin_id`: "123" (admin credentials to authorize registration)  
     - `admin_password`: "123"  

3. **Submit and Validate**  
   - Submits by sending `ENTER` on the admin password field.  
   - Waits briefly, then checks page source for error messages:  
     - "Employee ID already exists"  
     - "Invalid admin credentials"  
   - Logs success if no errors; otherwise proceeds with existing user.

### Step 1: User Login

1. **Navigate to the Login Page**  
   - URL: `http://localhost:5000/`  
   - Waits for the `employee_id` input.  

2. **Attempt Login with Test Account**  
   - Credentials:  
     - `employee_id`: "testuser"  
     - `password`: "password"  
   - Sends `ENTER` on password; waits for text "Employee:" on the inventory page.  
   - Logs success or moves to backup.

3. **Backup Login on Failure**  
   - Credentials:  
     - `employee_id`: "user"  
     - `password`: "pass"  
   - Repeats login sequence; confirms presence of "Employee:" text.

### Step 2: Add a New Inventory Item

1. **Open the Add Item Modal**  
   - Clicks the button with class `add-item-btn`.  
   - Retries up to 3 times on interception or unexpected alerts.  
   - Waits for modal ID `addItemModal` to be visible.  
   - Waits for auto-populated field `item_number` to have a non-empty value.

2. **Fill Item Form**  
   - Fields:  
     - `item_number`: (auto-generated, non-editable)  
     - `name`: "Test Game"  
     - `platform`: "PC"  
     - `original_packaging`: (checkbox) ensures checked  
     - `quality`: "Good"  
     - `stock`: "10"  
     - `price`: "20" (explicitly set to 20)

3. **Submit and Handle Alerts**  
   - Clicks submit button within `addItemModal` (`//div[@id='addItemModal']//button[@type='submit']`).  
   - Waits for alert; logs its text and accepts.  
   - On "already exists" alert, closes modal by clicking `.btn-close`.

4. **Verification**  
   - Checks element `#inventoryList` for text "Test Game"; logs presence or error.

### Step 3: Delete the Inventory Item

1. **Locate Item Card**  
   - Finds elements with class `inventory-item`.  
   - Identifies the card containing "Test Game".

2. **Trigger Deletion**  
   - Clicks `.delete-btn` on the item card.  
   - Logs the prompt alert text.

3. **Handle Confirmation Prompts**  
   - **Prompt Alert**: Sends keys "Delete"; accepts.  
   - **Final Confirmation**: Accepts subsequent alert.

4. **Post-Deletion Verification**  
   - Confirms "Test Game" is no longer in `#inventoryList`.

### Step 4: User Logout

1. **Logout Action**  
   - Clicks the button with class `logout-btn`.  
   - Waits for presence of the login page `employee_id` input.  
   - Logs "Logout succeeded".

## Test Termination

- After all steps (or on unexpected fatal error), invokes `driver.quit()` to close the browser.

## Logging and Delays

- Console prints indicate step progress and outcomes.  
- Uses `time.sleep()` between actions to allow UI stabilization and simulate user operating speed.

## Conclusion

Running this script as part of a continuous integration pipeline will enforce UI consistency across releases, catch regressions early, and increase overall confidence in the application's functionality. As the application evolves, this test suite can be extended with additional scenarios (e.g., editing items, verifying search functionality, or performance checks) to maintain comprehensive coverage. Ultimately, automated UI testing with this script contributes to faster development cycles, reduced manual QA effort, and a more reliable user experience.