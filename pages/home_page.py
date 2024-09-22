
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.my_account = (By.XPATH, locators['home_page']['my_account'])

    def go_to_my_account(self):
        self.click_element(self.my_account)
