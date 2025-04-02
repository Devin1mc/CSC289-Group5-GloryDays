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
    
    # --- Step 1: Verify Login Page ---
    driver.get("http://localhost:5000/")
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    print("Login page loaded successfully.")

    # Verify that login.css is loaded by checking for the link element
    login_css = driver.find_element(By.XPATH, "//link[contains(@href, 'login.css')]")
    if login_css:
        print("login.css is loaded.")
    else:
        print("login.css is NOT loaded.")

    # --- Step 2: Attempt Invalid Login ---
    # Clear and enter invalid credentials, then submit the form.
    emp_input = driver.find_element(By.NAME, "employee_id")
    pwd_input = driver.find_element(By.NAME, "password")
    emp_input.clear()
    pwd_input.clear()
    emp_input.send_keys("invalid_emp")
    pwd_input.send_keys("invalid_pass")
    pwd_input.send_keys(Keys.RETURN)
    
    # Wait briefly to allow the error message to appear
    time.sleep(2)
    page_text = driver.find_element(By.TAG_NAME, "body").text
    if "Invalid Employee ID or Password." in page_text:
        print("Invalid login correctly rejected.")
    else:
        print("Error: Expected invalid login error message not found.")

    # --- Step 3: Navigate to Registration Page ---
    driver.get("http://localhost:5000/register")
    wait.until(EC.presence_of_element_located((By.NAME, "first_name")))
    print("Registration page loaded successfully.")

    # --- Step 4: Fill Out and Submit Registration Form ---
    driver.find_element(By.NAME, "first_name").send_keys("Test")
    driver.find_element(By.NAME, "last_name").send_keys("User")
    driver.find_element(By.NAME, "employee_id").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("testpass")
    driver.find_element(By.NAME, "role").send_keys("user")  # Optional if the default is 'user'
    driver.find_element(By.NAME, "admin_id").send_keys("admin1")
    driver.find_element(By.NAME, "admin_password").send_keys("adminpass")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # --- Step 5: Verify Registration Success ---
    # Wait for redirection to the login page by checking for the login field
    wait.until(EC.presence_of_element_located((By.NAME, "employee_id")))
    current_url = driver.current_url
    if "login" in current_url.lower() or current_url.endswith("/"):
        print("Registration succeeded and user was redirected to the login page.")
    else:
        print("Error: Registration may have failed.")

    # --- Step 6: Perform Valid Login ---
    emp_input = driver.find_element(By.NAME, "employee_id")
    pwd_input = driver.find_element(By.NAME, "password")
    emp_input.clear()
    pwd_input.clear()
    emp_input.send_keys("testuser")
    pwd_input.send_keys("testpass")
    pwd_input.send_keys(Keys.RETURN)

    # Wait for redirection to inventory page by checking for "Employee:" text
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Employee:')]")))
    print("Valid login succeeded; inventory page loaded.")

finally:
    # Wait a short moment before closing to view final state
    time.sleep(2)
    driver.quit()
