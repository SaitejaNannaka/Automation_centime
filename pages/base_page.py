from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        """Initialize with WebDriver and a default timeout."""
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)
        self.timeout = timeout

    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Wait until the element disappears from the page."""
        timeout = timeout or self.timeout
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException as e:
            raise TimeoutError(f"Timeout waiting for element {locator} to disappear: {e}")

    def is_element_present(self, locator):
        """Check if an element is present on the page."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def enter_text(self, locator, text, retries=3):
        """Wait for element to be visible and enter text with retries."""
        for attempt in range(retries):
            try:
                element = self.wait_for_element(locator)
                element.clear()
                element.send_keys(text)
                return
            except (TimeoutException, ElementNotInteractableException) as e:
                if attempt == retries - 1:
                    raise TimeoutError(f"Failed to enter text in element {locator} after {retries} retries: {e}")

    def click_element(self, locator, retries=3):
        """Wait for element to be clickable and click with retries."""
        for attempt in range(retries):
            try:
                element = self.wait_for_clickable(locator)
                element.click()
                return
            except (TimeoutException, ElementNotInteractableException) as e:
                if attempt == retries - 1:
                    raise TimeoutError(f"Failed to click on element {locator} after {retries} retries: {e}")

    def select_dropdown_option(self, locator, value):
        """Select an option from a dropdown menu by visible text."""
        try:
            self.scroll_to_element(locator)
            self.click_element(locator)
            option_locator = (By.XPATH, f"//option[contains(text(), '{value}')]")
            self.click_element(option_locator)
        except Exception as e:
            raise Exception(f"Failed to select option '{value}' from dropdown {locator}: {e}")

    def wait_for_element(self, locator, timeout=None):
        """Wait until the element is present on the page."""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException as e:
            raise TimeoutError(f"Timeout while waiting for element {locator} to be present: {e}")

    def scroll_to_element(self, locator):
        """Scroll the page to bring the element into view."""
        try:
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            raise Exception(f"Failed to scroll to element {locator}: {e}")

    def click_element_using_js(self, locator):
        """Click on an element using JavaScript."""
        try:
            element = self.wait_for_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            raise Exception(f"Failed to click element {locator} using JavaScript: {e}")

    def is_element_clickable(self, locator):
        """Check if an element is clickable on the page."""
        try:
            self.wait_for_clickable(locator)
            return True
        except TimeoutException:
            return False

    def find_elements(self, locator):
        """Find all elements matching the given locator."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException as e:
            raise TimeoutError(f"Timeout while finding elements {locator}: {e}")

    def wait_for_clickable(self, locator, timeout=None):
        """Wait until the element is clickable."""
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException as e:
            raise TimeoutError(f"Element {locator} not clickable after {timeout} seconds: {e}")
