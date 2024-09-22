from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import uuid
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@pytest.mark.usefixtures("setup", "config", "locators", "data")
class TestRegistrationLogin:

    @pytest.fixture(autouse=True)
    def class_fixtures(self, config, locators, data):
        self.config = config
        self.locators = locators
        self.data = data

    def capture_screenshot_on_failure(self, test_name):
        """Capture a screenshot in case of failure."""
        screenshot_name = f"screenshots/{test_name}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"Screenshot captured: {screenshot_name}")

    def go_to_my_account(self):
        """Helper method to navigate to My Account page."""
        home_page = HomePage(self.driver, self.locators)
        home_page.go_to_my_account()

    def login_user(self, username, password):
        """Helper method to perform login."""
        login_page = LoginPage(self.driver, self.locators)
        login_page.login(username, password)

    def register_user(self, email, password):
        """Helper method to perform registration."""
        registration_page = RegistrationPage(self.driver, self.locators)
        registration_page.register(email, password)

    def open_base_url(self):
        """Helper method to open base URL."""
        self.driver.get(self.config['base_url'])

    def get_error_message(self):
        """Helper method to retrieve error messages."""
        error_message = self.driver.find_element(By.XPATH, "//ul[@class='woocommerce-error']//li").text.lower().strip()
        return error_message

    def verify_keywords_in_text(self, text, keywords, message):
        """Helper method to verify if at least one keyword is present in the text."""
        assert any(keyword in text for keyword in keywords), message

    def test_case_1_login(self):
        """Test case for user login."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.login_user(self.data['login']['username'], self.data['login']['password'])

            # Verify successful login
            assert "my account" in self.driver.page_source.lower(), "Login failed or 'My Account' not found in page source."

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_1_login")
            pytest.fail(f"Error during Test Case 1: {e}")

    def test_case_2_registration(self):
        """Test case for user registration."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.register_user(self.data['registration']['email'], self.data['registration']['password'])

            # Verify registration success
            try:
                logout_link = (By.LINK_TEXT, "Logout")
                assert self.driver.find_element(*logout_link), "Registration failed or 'Logout' link not found."
            except NoSuchElementException:
                self.verify_keywords_in_text(self.driver.page_source.lower(),
                                             ["thank you for registering"],
                                             "Registration failed or confirmation message not found.")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_2_registration")
            pytest.fail(f"Error during Test Case 2: {e}")

    def test_case_3_existing_user_registration(self):
        """Test case for existing user registration."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.register_user(self.data['existing_user']['email'], self.data['existing_user']['password'])

            # Verify error message for existing user
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["already registered"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_3_existing_user_registration")
            pytest.fail(f"Error during Test Case 3: {e}")

    def test_case_4_login_without_username_and_password(self):
        """Test case for login without entering username and password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.login_user("", "")  # Empty username and password

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["username is required"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_4_login_without_username_and_password")
            pytest.fail(f"Error during Test Case 4: {e}")

    def test_case_5_login_without_password(self):
        """Test case for login without entering password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.login_user(self.data['login']['username'], "")  # Empty password

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["password is required"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_5_login_without_password")
            pytest.fail(f"Error during Test Case 5: {e}")

    def test_case_6_login_without_username(self):
        """Test case for login without entering username."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.login_user("", self.data['login']['password'])  # Empty username

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["username is required"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_6_login_without_username")
            pytest.fail(f"Error during Test Case 6: {e}")

    def test_case_7_login_with_wrong_password(self):
        """Test case for login with an incorrect password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.login_user(self.data['login']['username'], "wrongpassword")  # Incorrect password

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["the password you entered for the username"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_7_login_with_wrong_password")
            pytest.fail(f"Error during Test Case 7: {e}")

    def test_case_8_register_without_email_and_password(self):
        """Test case for registration without entering email and password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.register_user("", "")  # Empty email and password

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["please provide a valid"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_8_register_without_email_and_password")
            pytest.fail(f"Error during Test Case 8: {e}")

    def test_case_9_register_without_password(self):
        """Test case for registration without entering password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            unique_email = f"testuser_{uuid.uuid4().hex[:6]}@example.com"
            self.register_user(unique_email, "")  # Empty password

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["please enter an account password"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_9_register_without_password")
            pytest.fail(f"Error during Test Case 9: {e}")

    def test_case_10_register_without_email(self):
        """Test case for registration without entering email."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.register_user("", self.data['registration']['password'])  # Empty email

            # Verify error message
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["error: please provide a valid  email address."], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_10_register_without_email")
            pytest.fail(f"Error during Test Case 10: {e}")

    def test_case_11_register_with_short_password(self):
        """Test case for registration with a very short password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            registration_page = RegistrationPage(self.driver, self.locators)
            registration_page.enter_text(registration_page.email_address, self.data['registration']['email'])
            registration_page.enter_text(registration_page.password, "12")  # Very short password

            # Click back on the email field to trigger validation
            registration_page.click_element(registration_page.email_address)
            self.driver.find_element(*registration_page.password).send_keys(Keys.ENTER)

            # Verify error message
            wait = WebDriverWait(self.driver, 10)
            error_message = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//div[contains(@class, 'woocommerce-password-strength') and contains(text(), 'stronger password')]"
            ))).text.lower().strip()

            self.verify_keywords_in_text(error_message, ["please enter a stronger password", "very weak"],
                                         f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_11_register_with_short_password")
            pytest.fail(f"Error during Test Case 11: {e}")

    def test_case_12_register_with_existing_email_and_password(self):
        """Test case for registration with an already existing email and password."""
        try:
            self.open_base_url()
            self.go_to_my_account()
            self.register_user(self.data['existing_user']['email'], self.data['existing_user']['password'])

            # Verify error message for existing email
            error_message = self.get_error_message()
            self.verify_keywords_in_text(error_message, ["account is already registered"], f"Unexpected error message: {error_message}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_12_register_with_existing_email_and_password")
            pytest.fail(f"Error during Test Case 12: {e}")
