import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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


def test_admin_login(driver):
    login(driver)
    heading = driver.find_element(By.XPATH, "//h1").text
    assert "Dashboard" in heading


def test_delete_product(driver):
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



def test_admin_logout(driver):
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
def test_add_new_category(driver):
    login(driver)

    try:
        # Go to Catalog > Categories
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Catalog')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Categories']"))
        ).click()

        # Click on Add New button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-original-title='Add New'], a[title='Add New']"))
        ).click()

        # Fill Category Info
        driver.find_element(By.ID, "input-name1").send_keys("Automation Category")
        driver.find_element(By.ID, "input-meta-title1").send_keys("Meta Title for Automation Category")

        # Save
        driver.find_element(By.CSS_SELECTOR, "button[data-original-title='Save']").click()

        # Verify success alert
        success = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "Success" in success.text

    except Exception as e:
        with open("category_creation_failure_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise e

def test_add_new_category(driver):
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

        # Fill in the General tab
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-name-1"))
        ).send_keys("Automation Test Category")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-meta-title-1"))
        ).send_keys("Meta Title for Automation Category")

        # Click the SEO tab and fill the Keyword
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='SEO']"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "category_seo_url[0][1]"))
        ).send_keys("automation-test-category")

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
