import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.testcase_id("TC-007")
def test_admin_login(driver):
    driver.get("http://localhost/opencart/admin")  # Adjust the URL as needed

    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    assert "Dashboard" in driver.title or "dashboard" in driver.current_url
import time

@pytest.mark.testcase_id("TC-008")
def test_add_new_product(driver):
    # Login first
    driver.get("http://localhost/opencart/admin")
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to Catalog > Products
    driver.find_element(By.ID, "menu-catalog").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[text()='Products']").click()

    # Click Add New
    driver.find_element(By.CSS_SELECTOR, "a[data-original-title='Add New']").click()

    # Fill in the form
    driver.find_element(By.ID, "input-name1").send_keys("Test Product")
    driver.find_element(By.ID, "input-meta-title1").send_keys("Test Product Meta Title")

    # Switch to Data tab
    driver.find_element(By.XPATH, "//a[text()='Data']").click()
    driver.find_element(By.ID, "input-model").send_keys("TP-001")

    # Save
    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()

    # Verify success message
    success = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
    assert "Success" in success

@pytest.mark.testcase_id("TC-009")
def test_delete_product(driver):
    # Login first
    driver.get("http://localhost/opencart/admin")
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to Products
    driver.find_element(By.ID, "menu-catalog").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[text()='Products']").click()

    # Search for the product
    driver.find_element(By.ID, "input-name").send_keys("Test Product")
    driver.find_element(By.ID, "button-filter").click()
    time.sleep(1)

    # Select and delete
    driver.find_element(By.NAME, "selected[]").click()
    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Delete']").click()
    alert = driver.switch_to.alert
    alert.accept()

    # Verify deletion
    success = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
    assert "Success" in success

@pytest.mark.testcase_id("TC-010")
def test_edit_product(driver):
    # Login first
    driver.get("http://localhost/opencart/admin")
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Navigate to Products
    driver.find_element(By.ID, "menu-catalog").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[text()='Products']").click()

    # Search for the product
    driver.find_element(By.ID, "input-name").send_keys("Test Product")
    driver.find_element(By.ID, "button-filter").click()
    time.sleep(1)

    # Click Edit icon
    driver.find_element(By.CSS_SELECTOR, "a[data-original-title='Edit']").click()

    # Edit Model name in Data tab
    driver.find_element(By.XPATH, "//a[text()='Data']").click()
    model_field = driver.find_element(By.ID, "input-model")
    model_field.clear()
    model_field.send_keys("TP-002")

    # Save
    driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()

    # Verify success message
    success = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
    assert "Success" in success

@pytest.mark.testcase_id("TC-011")
def test_admin_logout(driver):
    driver.get("http://localhost/opencart/admin")
    driver.find_element(By.ID, "input-username").send_keys("fatima")
    driver.find_element(By.ID, "input-password").send_keys("123968574")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Click Logout from top-right menu
    driver.find_element(By.CSS_SELECTOR, ".navbar-right a.dropdown-toggle").click()
    driver.find_element(By.XPATH, "//a[text()='Logout']").click()

    # Check if redirected to login page
    assert "Login" in driver.title or "login" in driver.current_url