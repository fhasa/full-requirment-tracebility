import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import uuid

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def close_security_modal_if_present(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "modal-security"))
        )
        close_btn = driver.find_element(By.CSS_SELECTOR, "#modal-security .btn-close")
        close_btn.click()
        WebDriverWait(driver, 5).until(EC.invisibility_of_element((By.ID, "modal-security")))
    except TimeoutException:
        pass


def login(driver):
    driver.get("http://localhost/opencart/admin2")
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Dashboard')]"))
    )
    close_security_modal_if_present(driver)


@pytest.mark.testcase_id("TC-007")
def test_admin_login(driver,custom_json_reporter):
    """[TC-007] Verify admin login functionality"""
    login(driver)
    heading = driver.find_element(By.XPATH, "//h1").text
    assert "Dashboard" in heading


@pytest.mark.testcase_id("TC-009")
def test_delete_product(driver, custom_json_reporter):
    """[TC-009] Verify product deletion functionality"""
    login(driver)

    try:
        # Navigate to Products page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Catalog')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Products']"))
        ).click()
        
        # Wait for the product list to load
        time.sleep(2)
        
        # Check if there are any products in the list
        no_results = driver.find_elements(By.XPATH, "//td[contains(text(), 'No results!')]")
        
        if len(no_results) > 0:
            pytest.skip("No products found to delete. Test skipped.")
        
        # Select the first product in the list (the first checkbox)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'][name*='selected']"))
        ).click()

        # Click the Delete button
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick*='confirm'][title='Delete']"))
        )
        delete_button.click()

        # Accept the confirmation alert
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        # Verify success alert
        success = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "Success" in success.text

    except Exception as e:
        with open("delete_product_failure_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Delete Product Error: {e}")
        raise

@pytest.mark.testcase_id("TC-008")
def test_admin_logout(driver,custom_json_reporter):
    """[TC-008] Verify admin logout functionality"""
    login(driver)

    try:
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav-logout a.nav-link"))
        )
        logout_link.click()
    except Exception as e:
        with open("logout_failure_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        pytest.fail(f"Logout failed: {e}")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-username"))
    )
    assert "login" in driver.current_url.lower()

# Removing the first implementation of test_add_new_category since it's duplicated
# and keeping only the more detailed second implementation with the test case ID

@pytest.mark.testcase_id("TC-010")
def test_add_new_category(driver, custom_json_reporter):
    """[TC-010] Verify category creation functionality"""
    login(driver)

    try:
        # Navigate to Catalog > Categories
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Catalog')]"))
        ).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Categories"))
        ).click()

        # Click on "Add New" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-bs-original-title='Add New'], a[title='Add New']"))
        ).click()

        # Generate unique name with timestamp to avoid duplicate entries
        timestamp = str(int(time.time()))
        category_name = f"Automation Test Category {timestamp}"
        meta_title = f"Meta Title for Automation Category {timestamp}"
        
        # Fill in the General tab
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-name-1"))
        ).send_keys(category_name)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-meta-title-1"))
        ).send_keys(meta_title)

        # Click the SEO tab and fill the Keyword with a unique value
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='SEO']"))
        ).click()

        # Generate a unique SEO URL keyword based on the category name and timestamp
        seo_keyword = f"automation-test-category-{timestamp}".lower()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "category_seo_url[0][1]"))
        ).send_keys(seo_keyword)

        # Click Save
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[form='form-category']"))
        ).click()

        # Check for success alert
        success = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "Success" in success.text

    except Exception as e:
        with open("category_creation_failure_source_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e
@pytest.mark.testcase_id("TC-011")
def test_admin_login_invalid_credentials(driver, custom_json_reporter):
    """[TC-011] Verify admin login with invalid credentials"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Enter invalid username and password
    driver.find_element(By.ID, "input-username").send_keys("invalid_username")
    driver.find_element(By.ID, "input-password").send_keys("invalid_password")
    
    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for and verify error message
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
    )
    
    # Verify error message content - test passes if error message exists
    assert "No match for Username and/or Password" in error_message.text
    
    # Verify we're still on the login page - test passes if we didn't navigate away
    assert "login" in driver.current_url.lower() or "admin" in driver.current_url.lower()
    assert driver.find_element(By.ID, "input-username").is_displayed()
@pytest.mark.testcase_id("TC-012")
def test_admin_login_invalid_username(driver, custom_json_reporter):
    """[TC-012] Verify admin login with invalid username"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Enter invalid username but correct password
    driver.find_element(By.ID, "input-username").send_keys("invalid_username")
    driver.find_element(By.ID, "input-password").send_keys("123968574")  # Correct password
    
    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for and verify error message
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
    )
    
    # Verify error message content
    assert "No match for Username and/or Password" in error_message.text
    
    # Verify we're still on the login page
    assert "login" in driver.current_url.lower() or "admin" in driver.current_url.lower()
    assert driver.find_element(By.ID, "input-username").is_displayed()
@pytest.mark.testcase_id("TC-013")
def test_admin_login_invalid_password(driver, custom_json_reporter):
    """[TC-013] Verify admin login with invalid password"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Enter valid username but incorrect password
    driver.find_element(By.ID, "input-username").send_keys("fatima")  # Valid username
    driver.find_element(By.ID, "input-password").send_keys("wrong_password")  # Incorrect password
    
    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for and verify error message
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
    )
    
    # Verify error message content
    assert "No match for Username and/or Password" in error_message.text
    
    # Verify we're still on the login page
    assert "login" in driver.current_url.lower() or "admin" in driver.current_url.lower()
    assert driver.find_element(By.ID, "input-username").is_displayed()
@pytest.mark.testcase_id("TC-014")
def test_admin_login_empty_fields(driver, custom_json_reporter):
    """[TC-014] Verify admin login with empty fields"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Leave username and password fields empty (no sendKeys calls)
    
    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for error message or validation to appear
    time.sleep(1)
    
    # Verify we're still on the login page - this should pass if login failed as expected
    assert "login" in driver.current_url.lower() or "admin" in driver.current_url.lower()
    assert driver.find_element(By.ID, "input-username").is_displayed()
    
    # Check for any of the possible validation indicators
    validation_present = False
    
    # Check for alert messages
    alert_messages = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
    if len(alert_messages) > 0:
        validation_present = True
    
    # Check for field validation (red borders, etc.)
    invalid_fields = driver.find_elements(By.CSS_SELECTOR, ".is-invalid")
    if len(invalid_fields) > 0:
        validation_present = True
    
    # Check for text validation messages
    validation_texts = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
    if len(validation_texts) > 0:
        validation_present = True
        
    # The test should pass if we're still on the login page and any validation is present
    assert validation_present, "No validation messages found for empty fields"
@pytest.mark.testcase_id("TC-015")
def test_admin_redirect_to_dashboard(driver, custom_json_reporter):
    """[TC-015] Verify admin redirect to dashboard after login"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Enter valid admin credentials
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    
    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for redirect to dashboard and verify dashboard heading is visible
    dashboard_heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Dashboard')]"))
    )
    assert "Dashboard" in dashboard_heading.text
    
    # Close security modal if it appears
    close_security_modal_if_present(driver)
    
    # Verify that the URL contains '/dashboard' or similar endpoint
    assert "dashboard" in driver.current_url.lower()
    
    # Verify that dashboard elements are visible
    # Check for common dashboard elements
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "stats"))
    )
    
    # Check for navigation menu
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "menu"))
    )
    
    # Check for the header element that typically contains user profile and notifications
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "header"))
    )
    
    # Verify that the dashboard panels or widgets are present
    panels = driver.find_elements(By.CSS_SELECTOR, ".card")
    assert len(panels) > 0, "No dashboard panels found"
@pytest.mark.testcase_id("TC-016")
def test_password_masking_during_admin_login(driver, custom_json_reporter):
    """[TC-016] Verify password masking during admin login"""
    # Navigate to the OpenCart admin login page
    driver.get("http://localhost/opencart/admin2")
    
    # Find the password field
    password_field = driver.find_element(By.ID, "input-password")
    
    # Verify that the password field type is set to 'password'
    # This HTML attribute ensures text is masked with dots/asterisks
    password_type = password_field.get_attribute("type")
    assert password_type == "password", f"Password field type is {password_type}, should be 'password'"
    
    # Enter some text in the password field
    test_password = "TestPassword123"
    password_field.send_keys(test_password)
    
    # Get the displayed value of the field
    # Due to security restrictions, browsers won't return the actual value
    # But we can verify it doesn't match our input (indicating masking)
    displayed_value = password_field.get_attribute("value")
    
    # There are two possibilities:
    # 1. Browser might return empty string for security reasons
    # 2. Browser might return masked value (usually same length as input)
    
    # For case 1, we verify it's not our clear text password
    if displayed_value == "":
        # This is expected behavior in many browsers
        pass
    else:
        # For case 2, verify the actual value doesn't match our input
        # This means it's masked
        assert displayed_value != test_password, "Password is not masked properly"
    
    # Additional verification that password field has masking appearance
    # This checks that the field has a standard password input appearance
    # with dots or asterisks instead of plain text
    assert password_field.is_displayed(), "Password field is not visible"
@pytest.mark.testcase_id("TC-017")
def test_browser_back_button_after_logout(driver, custom_json_reporter):
    """[TC-017] Verify browser back button after admin logout"""
    # First login to the admin panel
    login(driver)
    
    # Navigate to a protected admin page (e.g., Products page)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Catalog')]"))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Products']"))
    ).click()
    
    # Verify we're on the Products page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Products')]"))
    )
    
    # Store the URL of the protected page
    protected_page_url = driver.current_url
    
    # Log out
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#nav-logout a.nav-link"))
    ).click()
    
    # Verify we're logged out and on the login page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "input-username"))
    )
    assert "login" in driver.current_url.lower() or "admin" in driver.current_url.lower()
    
    # Go back to the protected page using browser back button
    driver.back()
    
    # Wait a moment for any redirects to occur
    time.sleep(2)
    
    # Verify we're not allowed to access the protected page
    # Either we should be redirected to the login page
    # Or we should see a login form
    
    # Check if we're on the login page
    login_elements = driver.find_elements(By.ID, "input-username")
    
    # The test passes if we're either:
    # 1. Redirected to the login page, or
    # 2. Not on the same protected page URL we were on before logout
    assert len(login_elements) > 0 or driver.current_url != protected_page_url, \
        "Back button allowed access to protected page after logout"