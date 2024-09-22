from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
import pytest
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.billing_address_page import BillingAddressPage
from pages.shipping_address_page import ShippingAddressPage


@pytest.mark.usefixtures("setup", "config", "locators", "data")
class TestAddressManagement:

    @pytest.fixture(autouse=True)
    def class_fixtures(self, config, locators, data):
        """Assign fixtures to class attributes for easy access."""
        self.config = config
        self.locators = locators
        self.data = data

    def capture_screenshot_on_failure(self, test_name):
        """Capture a screenshot in case of failure."""
        screenshot_name = f"screenshots/{test_name}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"Screenshot captured: {screenshot_name}")

    def register_user(self):
        """Register a new user and return the email and password."""
        home_page = HomePage(self.driver, self.locators)
        registration_page = RegistrationPage(self.driver, self.locators)

        # Open the base URL and go to My Account
        self.driver.get(self.config['base_url'])
        home_page.go_to_my_account()

        # Register a new user
        new_email = self.data['registration']['email']
        new_password = self.data['registration']['password']
        registration_page.register(new_email, new_password)

        return new_email, new_password

    def verify_success_message(self, expected_keywords):
        """Verify the success message after saving the address."""
        success_message_locator = (By.XPATH, "//div[contains(@class, 'woocommerce-message') and contains(text(), 'Address changed successfully.')]")
        success_message = self.driver.find_element(*success_message_locator).text.lower().strip()
        assert any(keyword in success_message for keyword in expected_keywords), \
            f"Expected to find one of {expected_keywords} in the success message, but got '{success_message}'."

    def verify_error_messages(self, expected_messages):
        """Verify that all required field error messages are displayed."""
        error_message_locator = (By.XPATH, "//ul[@class='woocommerce-error']//li")
        actual_error_messages = [message.text.strip() for message in self.driver.find_elements(*error_message_locator)]
        for expected_message in expected_messages:
            assert any(expected_message in actual_message for actual_message in actual_error_messages), \
                f"Expected error message '{expected_message}' not found in actual messages: {actual_error_messages}"

    def test_case_13_add_billing_address(self):
        """
        Add a billing address and verify the success message.
        """
        try:
            self.register_user()
            billing_address_page = BillingAddressPage(self.driver, self.locators)

            # Navigate to the billing address section and enter details
            billing_address_page.go_to_addresses_section()
            billing_address_page.go_to_billing_address()
            billing_address_page.enter_billing_address(self.data['billing_address'])
            billing_address_page.save_address()

            # Verify success message
            self.verify_success_message(["address changed successfully"])

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_13_add_billing_address")
            pytest.fail(f"Error during Test Case 13: {e}")

    def test_case_14_add_shipping_address(self):
        """
        Add a shipping address and verify the success message.
        """
        try:
            self.register_user()
            shipping_address_page = ShippingAddressPage(self.driver, self.locators)

            # Navigate to the shipping address section and enter details
            shipping_address_page.go_to_addresses_section()
            shipping_address_page.go_to_shipping_address()
            shipping_address_page.enter_shipping_address(self.data['shipping_address'])
            shipping_address_page.save_address()

            # Verify success message
            self.verify_success_message(["address changed successfully"])

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_14_add_shipping_address")
            pytest.fail(f"Error during Test Case 14: {e}")

    def test_case_15_empty_billing_address_fields(self):
        """
        Try saving an empty billing address and verify the error messages.
        """
        try:
            self.register_user()
            billing_address_page = BillingAddressPage(self.driver, self.locators)

            # Navigate to the billing address section and try saving without entering data
            billing_address_page.go_to_addresses_section()
            billing_address_page.go_to_billing_address()
            billing_address_page.scroll_to_element(billing_address_page.save_button)
            billing_address_page.save_address()

            # Verify all required field error messages
            expected_messages = [
                "First Name is a required field.",
                "Last Name is a required field.",
                "Phone is a required field.",
                "Address is a required field.",
                "Town / City is a required field.",
                "Postcode / ZIP is a required field."
            ]
            self.verify_error_messages(expected_messages)

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_15_empty_billing_address_fields")
            pytest.fail(f"Error during Test Case 15: {e}")

    def test_case_16_empty_shipping_address_fields(self):
        """
        Try saving an empty shipping address and verify the error messages.
        """
        try:
            self.register_user()
            shipping_address_page = ShippingAddressPage(self.driver, self.locators)

            # Navigate to the shipping address section and try saving without entering data
            shipping_address_page.go_to_addresses_section()
            shipping_address_page.go_to_shipping_address()
            shipping_address_page.scroll_to_element(shipping_address_page.save_button)
            shipping_address_page.save_address()

            # Verify all required field error messages
            expected_messages = [
                "First Name is a required field.",
                "Last Name is a required field.",
                "Address is a required field.",
                "Town / City is a required field.",
                "Postcode / ZIP is a required field."
            ]
            self.verify_error_messages(expected_messages)

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_16_empty_shipping_address_fields")
            pytest.fail(f"Error during Test Case 16: {e}")
