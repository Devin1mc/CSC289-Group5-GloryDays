from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

try:
    wait = WebDriverWait(driver, 10)
    
    # === Step 1: Login ===
    driver.get("http://localhost:5000/")
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    print("Login page loaded successfully.")
    time.sleep(2)
    
    # Clear and fill username (employee_id) with "user"
    emp_input = driver.find_element(By.NAME, "employee_id")
    emp_input.clear()
    emp_input.send_keys("user")
    time.sleep(2)
    
    # Clear and fill password with "pass"
    pwd_input = driver.find_element(By.NAME, "password")
    pwd_input.clear()
    pwd_input.send_keys("pass")
    time.sleep(2)
    
    # Submit the login form
    pwd_input.send_keys(Keys.RETURN)
    time.sleep(2)
    
    # Wait for inventory page to load (check for "Employee:" text)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Employee:')]")))
    print("Valid login succeeded; inventory page loaded.")
    time.sleep(2)

    # === Step 2: Add a New Inventory Item ===
    add_item_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-item-btn")))
    add_item_btn.click()
    print("Clicked 'Add Item' button.")
    time.sleep(2)
    
    # Wait for the Add Item modal to appear
    wait.until(EC.visibility_of_element_located((By.ID, "addItemModal")))
    print("Add Item modal is visible.")
    time.sleep(2)
    
    # Fill out the add item form
    driver.find_element(By.ID, "sku").send_keys("TESTSKU")
    driver.find_element(By.ID, "name").send_keys("Test Game")
    driver.find_element(By.ID, "platform").send_keys("PC")
    packaging_checkbox = driver.find_element(By.ID, "original_packaging")
    if not packaging_checkbox.is_selected():
        packaging_checkbox.click()
    driver.find_element(By.ID, "quality").send_keys("Good")
    driver.find_element(By.ID, "stock").send_keys("10")
    time.sleep(2)
    
    # Submit the form within the modal
    add_submit_btn = driver.find_element(By.XPATH, "//div[@id='addItemModal']//button[@type='submit']")
    add_submit_btn.click()
    time.sleep(2)
    
    # Wait for and handle the alert that confirms addition or error
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert_text = alert.text
    print("Add Item alert message:", alert_text)
    alert.accept()
    time.sleep(2)
    
    # If the item already exists, close the modal to clear the overlay
    if "already exists" in alert_text:
        try:
            modal = driver.find_element(By.ID, "addItemModal")
            if modal.is_displayed():
                close_btn = modal.find_element(By.CLASS_NAME, "btn-close")
                close_btn.click()
                wait.until(EC.invisibility_of_element_located((By.ID, "addItemModal")))
                print("Add Item modal closed after 'item already exists' alert.")
        except Exception as e:
            print("Failed to close add modal:", e)
    time.sleep(2)  # Allow time for inventory list refresh

    # Verify the item is present in the inventory list
    inventory_list = driver.find_element(By.ID, "inventoryList")
    if "TESTSKU" in inventory_list.text:
        print("Inventory item is present (either newly added or pre-existing).")
    else:
        print("Error: Inventory item not found.")
    time.sleep(2)

    # === Step 3: Delete the Inventory Item ===
    # Ensure any modal is fully closed before proceeding
    wait.until(EC.invisibility_of_element_located((By.ID, "addItemModal")))
    time.sleep(2)
    
    # Locate and click the delete button for the item with SKU "TESTSKU"
    delete_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'delete-btn') and @data-sku='TESTSKU']")
    if delete_buttons:
        delete_buttons[0].click()
        print("Clicked Delete button for item 'TESTSKU'.")
    else:
        print("Error: Delete button for 'TESTSKU' not found.")
    time.sleep(2)
    
    # Handle the JavaScript prompt: send the confirmation text "Delete"
    wait.until(EC.alert_is_present())
    prompt_alert = driver.switch_to.alert
    print("Delete prompt message:", prompt_alert.text)
    prompt_alert.send_keys("Delete")
    prompt_alert.accept()
    time.sleep(2)
    
    # Accept the subsequent deletion confirmation alert
    wait.until(EC.alert_is_present())
    del_confirm_alert = driver.switch_to.alert
    print("Delete confirmation alert message:", del_confirm_alert.text)
    del_confirm_alert.accept()
    time.sleep(2)  # Allow time for deletion
    
    # Verify the item is deleted
    inventory_list = driver.find_element(By.ID, "inventoryList")
    if "TESTSKU" not in inventory_list.text:
        print("Inventory item deleted successfully.")
    else:
        print("Error: Inventory item still present after deletion.")
    time.sleep(2)

    # === Step 4: Logout ===
    logout_btn = driver.find_element(By.CLASS_NAME, "logout-btn")
    logout_btn.click()
    print("Clicked Logout button.")
    time.sleep(2)
    
    # Wait for redirection to the login page
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    print("Logout succeeded; login page loaded.")
    time.sleep(2)

finally:
    time.sleep(2)
    driver.quit()
