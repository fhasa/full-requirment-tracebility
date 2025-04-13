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
def test_delete_product(driver,custom_json_reporter):
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

        # Search for the product by name
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-name"))
        ).send_keys("Test Product")

        driver.find_element(By.ID, "button-filter").click()

        # Wait for the checkbox to appear and select the product
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'][name*='selected']"))
        ).click()

        # Click the Delete button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-original-title='Delete'], button[title='Delete']"))
        ).click()

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