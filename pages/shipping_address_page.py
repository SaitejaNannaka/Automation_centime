from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

class ShippingAddressPage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.address_link = (By.XPATH, locators['shipping_address_page']['address'])
        self.shipping_address_link = (By.XPATH, locators['shipping_address_page']['shipping_address'])
        self.first_name = (By.XPATH, locators['shipping_address_page']['first_name'])
        self.last_name = (By.XPATH, locators['shipping_address_page']['last_name'])
        self.company_name = (By.XPATH, locators['shipping_address_page']['company_name'])
        # self.email = (By.XPATH, locators['shipping_address_page']['email'])
        # self.phone = (By.XPATH, locators['shipping_address_page']['phone'])
        self.country = (By.XPATH, locators['shipping_address_page']['country'])
        self.country_search_input = (By.XPATH, locators['shipping_address_page']['country_search_input'])
        self.address_1 = (By.XPATH, locators['shipping_address_page']['address_1'])
        self.address_2 = (By.XPATH, locators['shipping_address_page']['address_2'])
        self.city = (By.XPATH, locators['shipping_address_page']['city'])
        self.state = (By.XPATH, locators['shipping_address_page']['state'])
        self.state_search_input = (By.XPATH, locators['shipping_address_page']['state_search_input'])
        self.postcode = (By.XPATH, locators['shipping_address_page']['postcode'])
        self.save_button = (By.XPATH, locators['shipping_address_page']['save_button'])

    def go_to_addresses_section(self):
        self.click_element(self.address_link)

    def go_to_shipping_address(self):
        self.click_element(self.shipping_address_link)

    def enter_shipping_address(self, address_data):
        self.enter_text(self.first_name, address_data['first_name'])
        self.enter_text(self.last_name, address_data['last_name'])
        self.enter_text(self.company_name, address_data['company_name'])
        # self.enter_text(self.email, address_data['email'])
        # self.enter_text(self.phone, address_data['phone'])

        # Country selection: click on country dropdown and search for the country
        self.click_element(self.country)  # Click to open the country dropdown

        # Wait for the input field inside the dropdown to be present
        country_search_input = self.wait_for_element(self.country_search_input)

        # Enter the country name and hit ENTER to select it
        country_search_input.send_keys(address_data['country'])
        country_search_input.send_keys(Keys.ENTER)

        self.enter_text(self.address_1, address_data['address_1'])
        self.enter_text(self.address_2, address_data['address_2'])
        self.enter_text(self.city, address_data['city'])

        # Scroll to the state field before clicking for other countries
        self.scroll_to_element(self.state)

        # Use JavaScript to click on the state field if it’s not clickable traditionally
        self.click_element_using_js(self.state)

        # Directly enter the state name for other countries
        self.enter_text(self.state, address_data['state'])


        # Enter the postcode
        self.enter_text(self.postcode, address_data['postcode'])

    def save_address(self):
        self.click_element(self.save_button)
