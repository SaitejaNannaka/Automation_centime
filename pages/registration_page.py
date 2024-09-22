from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

class RegistrationPage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.email_address = (By.XPATH, locators['registration_page']['email_address'])
        self.password = (By.XPATH, locators['registration_page']['password'])
        self.register_button = (By.XPATH, locators['registration_page']['register_button'])

    def register(self, email, password):
        # Step 1: Wait for email field and enter email
        self.enter_text(self.email_address, email)

        # Step 2: Wait for password field and enter password
        self.enter_text(self.password, password)


        # Optional: Wait a little for the form to validate
        time.sleep(2)
        # Step 4: Click on the register button
        self.click_element(self.email_address)
        # Step 4: Click on the register button
        self.click_element(self.register_button)
