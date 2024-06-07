from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


# Setup function to initialize the WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver


# Teardown function to close the WebDriver
def teardown_driver(driver):
    driver.quit()


# Test function for Basic Auth page
def test_basic_auth():
    driver = setup_driver()
    try:
        url = "https://admin:admin@the-internet.herokuapp.com/basic_auth"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Validate successful login by checking the page content
        content = driver.find_element(By.TAG_NAME, "p").text
        assert "Congratulations" in content, "Login failed or content not found."
        print("Basic Auth test passed successfully.")
    finally:
        teardown_driver(driver)


# Test function for Checkboxes page
def test_checkboxes():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/checkboxes"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Locate checkboxes
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

        # Debugging: Print the number of checkboxes found
        print(f"Found {len(checkboxes)} checkboxes.")

        # Check if checkboxes were found
        if not checkboxes:
            raise Exception("No checkboxes found on the page.")

        # Tick all checkboxes and validate
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
                time.sleep(1)  # Adding sleep to observe the checkbox click
            assert checkbox.is_selected(), "Checkbox is not selected."
        print("Checkboxes test passed successfully.")
    finally:
        teardown_driver(driver)


# Test function for Add/Remove Elements page
def test_add_remove_elements():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/add_remove_elements/"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Add element
        add_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='addElement()']")
        add_button.click()
        time.sleep(1)  # Adding sleep to observe the button click

        # Validate element is added
        added_element = driver.find_element(By.CSS_SELECTOR, "div#elements button")
        assert added_element.is_displayed(), "Element was not added."

        # Remove element
        added_element.click()
        time.sleep(1)  # Adding sleep to observe the button click

        # Validate element is removed
        elements = driver.find_elements(By.CSS_SELECTOR, "div#elements button")
        assert len(elements) == 0, "Element was not removed."
        print("Add/Remove Elements test passed successfully.")
    finally:
        teardown_driver(driver)


# Test function for Dropdown page
def test_dropdown():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/dropdown"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        dropdown = driver.find_element(By.ID, "dropdown")

        # Select option 1
        dropdown.find_element(By.CSS_SELECTOR, "option[value='1']").click()
        time.sleep(1)  # Adding sleep to observe the dropdown selection
        selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[value='1']")
        assert selected_option.is_selected(), "Option 1 is not selected."

        # Select option 2
        dropdown.find_element(By.CSS_SELECTOR, "option[value='2']").click()
        time.sleep(1)  # Adding sleep to observe the dropdown selection
        selected_option = dropdown.find_element(By.CSS_SELECTOR, "option[value='2']")
        assert selected_option.is_selected(), "Option 2 is not selected."
        print("Dropdown test passed successfully.")
    finally:
        teardown_driver(driver)


# Test function for Form Authentication page
def test_form_authentication():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/login"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Enter username and password
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        time.sleep(1)  # Adding sleep to observe the input
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        time.sleep(1)  # Adding sleep to observe the input
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)  # Allowing time for the login to process

        # Validate successful login
        flash_message = driver.find_element(By.ID, "flash").text
        assert "You logged into a secure area!" in flash_message, "Login failed."
        print("Form Authentication test passed successfully.")
    finally:
        teardown_driver(driver)


# Test function for JavaScript Alerts page
def test_javascript_alerts():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/javascript_alerts"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Click button to trigger alert
        driver.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
        time.sleep(1)  # Adding sleep to observe the alert

        # Handle alert
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "I am a JS Alert" in alert_text, "Alert text does not match."
        alert.accept()
        time.sleep(1)  # Adding sleep to observe the alert accept

        # Validate result text
        result_text = driver.find_element(By.ID, "result").text
        assert "You successfully clicked an alert" in result_text, "Result text does not match."
        print("JavaScript Alerts test passed successfully.")
    finally:
        teardown_driver(driver)


def test_hovers():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/hovers"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Hover over the first image
        image = driver.find_elements(By.CSS_SELECTOR, ".figure")[0]
        actions = ActionChains(driver)
        actions.move_to_element(image).perform()

        # Validate the additional information
        info = driver.find_element(By.CSS_SELECTOR, ".figcaption h5").text
        assert "name: user1" in info, "Hover info not displayed correctly."
        print("Hovers test passed successfully.")
    finally:
        teardown_driver(driver)


def test_notification_messages():
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/notification_message_rendered"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Click on the link to trigger a notification
        driver.find_element(By.LINK_TEXT, "Click here").click()
        time.sleep(2)  # Allow time for the notification to appear

        # Validate the notification message
        notification_message = driver.find_element(By.ID, "flash").text
        assert "Action" in notification_message, "Notification message not found."
        print("Notification Messages test passed successfully.")
    finally:
        teardown_driver(driver)


def test_javascript_onload_event_error() -> object:
    driver = setup_driver()
    try:
        url = "https://the-internet.herokuapp.com/javascript_error"
        driver.get(url)

        # Allow time for the page to load
        time.sleep(2)

        # Validate the error message
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "This page has a JavaScript error in the onload event" in body_text, "JavaScript error message not found."
        print("JavaScript onload event error test passed successfully.")
    finally:
        teardown_driver(driver)


# Run the test cases
test_basic_auth()
test_checkboxes()
test_add_remove_elements()
test_dropdown()
test_form_authentication()
test_javascript_alerts()
test_hovers()
test_notification_messages()
test_javascript_onload_event_error()