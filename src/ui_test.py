from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException,
    NoAlertPresentException,
    ElementClickInterceptedException,
)
import time

def slow_type(element, text, delay=0.1):
    """Type text slowly into an element to simulate normal typing speed."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    wait = WebDriverWait(driver, 10)

    # === Step 0: Registration ===
    try:
        driver.get("http://localhost:5000/register")
        wait.until(EC.presence_of_element_located((By.NAME, "first_name")))
        print("Step 0: Registration page loaded successfully.")
        
        # Fill out the registration form for the test user using slow typing
        first_name_field = driver.find_element(By.NAME, "first_name")
        first_name_field.clear()
        slow_type(first_name_field, "Test")
        
        last_name_field = driver.find_element(By.NAME, "last_name")
        last_name_field.clear()
        slow_type(last_name_field, "User")
        
        employee_field = driver.find_element(By.NAME, "employee_id")
        employee_field.clear()
        slow_type(employee_field, "testuser")
        
        password_field = driver.find_element(By.NAME, "password")
        password_field.clear()
        slow_type(password_field, "password")
        
        # Fill admin credentials to authorize the registration
        admin_id_field = driver.find_element(By.NAME, "admin_id")
        admin_id_field.clear()
        slow_type(admin_id_field, "123")
        
        admin_password_field = driver.find_element(By.NAME, "admin_password")
        admin_password_field.clear()
        slow_type(admin_password_field, "123")
        
        # Submit the registration form by sending ENTER from the last field
        admin_password_field.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # Check if registration failed due to duplicate employee id or admin error
        page_source = driver.page_source
        if "Employee ID already exists" in page_source or "Invalid admin credentials" in page_source:
            print("Step 0: Registration not successful (user may already be registered or admin credentials invalid). Continuing with test...")
        else:
            print("Step 0: Registration successful, redirected to login.")
    except Exception as e:
        print("Step 0: Registration step encountered an error:", e)
    
    # === Step 1: Login ===
    # First, try logging in with test account credentials.
    driver.get("http://localhost:5000/")
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    print("Step 1: Login page loaded successfully.")
    time.sleep(2)
    
    login_employee_field = driver.find_element(By.NAME, "employee_id")
    login_employee_field.clear()
    login_employee_field.send_keys("testuser")
    
    login_password_field = driver.find_element(By.NAME, "password")
    login_password_field.clear()
    login_password_field.send_keys("password")
    time.sleep(1)
    login_password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Employee:')]")))
        print("Step 1: Valid login succeeded with test account ('testuser').")
    except TimeoutException:
        print("Step 1: Login with test account failed. Trying backup credentials ('user'/'pass').")
        # Try backup credentials
        driver.get("http://localhost:5000/")
        wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
        login_employee_field = driver.find_element(By.NAME, "employee_id")
        login_employee_field.clear()
        login_employee_field.send_keys("user")
        
        login_password_field = driver.find_element(By.NAME, "password")
        login_password_field.clear()
        login_password_field.send_keys("pass")
        time.sleep(1)
        login_password_field.send_keys(Keys.RETURN)
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Employee:')]")))
        print("Step 1: Valid login succeeded with backup credentials ('user'/'pass').")
    time.sleep(2)
    
    # === Step 2: Add a New Inventory Item ===
    max_attempts = 3
    attempt = 0
    modal_ready = False
    while attempt < max_attempts and not modal_ready:
        attempt += 1
        try:
            # Attempt to click the "Add Item" button
            add_item_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-item-btn")))
            try:
                add_item_btn.click()
                print(f"Step 2: Clicked 'Add Item' button (attempt {attempt}).")
            except ElementClickInterceptedException as e:
                # If clicking is intercepted, check if modal is already open.
                try:
                    modal = driver.find_element(By.ID, "addItemModal")
                    if modal.is_displayed():
                        print(f"Step 2: 'Add Item' modal is already open (attempt {attempt}).")
                        modal_ready = True
                        break
                    else:
                        raise e
                except Exception as inner_e:
                    raise e
            time.sleep(2)
            
            # Wait for the Add Item modal to appear
            wait.until(EC.visibility_of_element_located((By.ID, "addItemModal")))
            print(f"Step 2: 'Add Item' modal is visible (attempt {attempt}).")
            time.sleep(1)
            
            # Wait until the auto-populated 'item_number' field is visible and non-empty
            wait.until(EC.visibility_of_element_located((By.ID, "item_number")))
            wait.until(lambda d: d.find_element(By.ID, "item_number").get_attribute("value") != "")
            print(f"Step 2: 'Item Number' field is populated (attempt {attempt}).")
            modal_ready = True
            
        except (TimeoutException, UnexpectedAlertPresentException) as e:
            try:
                alert = driver.switch_to.alert
                print(f"Step 2: Unexpected alert on attempt {attempt}: {alert.text}")
                alert.accept()
            except NoAlertPresentException:
                print(f"Step 2: No alert present on attempt {attempt} while handling exception.")
            time.sleep(2)
            # Do not refresh; simply wait and retry.
    
    if not modal_ready:
        print("Step 2: Failed to open 'Add Item' modal after maximum attempts.")
        driver.quit()
        exit(1)
    
    time.sleep(2)
    
    # Fill out the Add Item form (the "item_number" is auto-populated)
    driver.find_element(By.ID, "name").send_keys("Test Game")
    driver.find_element(By.ID, "platform").send_keys("PC")
    packaging_checkbox = driver.find_element(By.ID, "original_packaging")
    if not packaging_checkbox.is_selected():
        packaging_checkbox.click()
    driver.find_element(By.ID, "quality").send_keys("Good")
    driver.find_element(By.ID, "stock").send_keys("10")
    # Set the price field to "20" instead of "19.99"
    driver.find_element(By.ID, "price").send_keys("20")
    print("Step 2: Filled out the Add Item form.")
    time.sleep(2)
    
    # Click the submit button within the modal
    add_submit_btn = driver.find_element(By.XPATH, "//div[@id='addItemModal']//button[@type='submit']")
    add_submit_btn.click()
    print("Step 2: Submitted the Add Item form.")
    time.sleep(2)
    
    # Wait for and handle the add item alert
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"Step 2: Add Item alert message: {alert_text}")
    alert.accept()
    time.sleep(2)
    
    # If alert indicates the item already exists, try closing the modal
    if "already exists" in alert_text:
        try:
            modal = driver.find_element(By.ID, "addItemModal")
            if modal.is_displayed():
                close_btn = modal.find_element(By.CLASS_NAME, "btn-close")
                close_btn.click()
                wait.until(EC.invisibility_of_element_located((By.ID, "addItemModal")))
                print("Step 2: Closed 'Add Item' modal after 'item already exists' alert.")
        except Exception as e:
            print("Step 2: Exception when closing modal:", e)
    time.sleep(2)
    
    # Verify that "Test Game" appears in the inventory list
    inventory_list = driver.find_element(By.ID, "inventoryList")
    if "Test Game" in inventory_list.text:
        print("Step 2: Inventory item 'Test Game' is present.")
    else:
        print("Step 2: Error: Inventory item 'Test Game' not found.")
    time.sleep(2)
    
    # === Step 3: Delete the Inventory Item ===
    inventory_items = driver.find_elements(By.CLASS_NAME, "inventory-item")
    item_deleted = False
    for item in inventory_items:
        if "Test Game" in item.text:
            try:
                delete_btn = item.find_element(By.CLASS_NAME, "delete-btn")
                delete_btn.click()
                print("Step 3: Clicked Delete button for 'Test Game'.")
                item_deleted = True
                break
            except Exception as e:
                print("Step 3: Error finding Delete button for 'Test Game':", e)
    if not item_deleted:
        print("Step 3: Error: Inventory card for 'Test Game' not found.")
    time.sleep(2)
    
    # Handle the deletion confirmation prompt alert (type "Delete")
    wait.until(EC.alert_is_present())
    prompt_alert = driver.switch_to.alert
    print(f"Step 3: Delete prompt alert message: {prompt_alert.text}")
    prompt_alert.send_keys("Delete")
    prompt_alert.accept()
    time.sleep(2)
    
    # Handle the final deletion confirmation alert
    wait.until(EC.alert_is_present())
    del_confirm_alert = driver.switch_to.alert
    print(f"Step 3: Delete confirmation alert message: {del_confirm_alert.text}")
    del_confirm_alert.accept()
    time.sleep(2)
    
    # Verify the item is no longer present
    inventory_list = driver.find_element(By.ID, "inventoryList")
    if "Test Game" not in inventory_list.text:
        print("Step 3: Inventory item 'Test Game' deleted successfully.")
    else:
        print("Step 3: Error: Inventory item 'Test Game' still present after deletion.")
    time.sleep(2)
    
    # === Step 4: Logout ===
    logout_btn = driver.find_element(By.CLASS_NAME, "logout-btn")
    logout_btn.click()
    print("Step 4: Clicked Logout button.")
    time.sleep(2)
    
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    print("Step 4: Logout succeeded; login page loaded.")
    time.sleep(2)
    
finally:
    time.sleep(2)
    driver.quit()
