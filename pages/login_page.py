
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.username = (By.XPATH, locators['login_page']['username'])
        self.password = (By.XPATH, locators['login_page']['password'])
        self.login_button = (By.XPATH, locators['login_page']['login_button'])

    def login(self, username, password):
        self.enter_text(self.username, username)
        self.enter_text(self.password, password)
        self.click_element(self.login_button)
