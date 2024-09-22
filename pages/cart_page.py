from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.view_cart_button = (By.XPATH, locators['cart_page']['cart'])

    def go_to_cart(self):
        self.click_element(self.view_cart_button)

    def is_element_present(self, locator):
        """Check if an element is present on the page."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    def remove_product_from_cart(self, product_name):
        try:
            # Scroll to the product remove button to make it visible
            remove_button_locator = (By.XPATH, f"//tr[contains(., '{product_name}')]//a[contains(@class, 'remove')]")
            self.scroll_to_element(remove_button_locator)

            # Use JavaScript to click the remove button if it's not clickable normally
            self.click_element_using_js(remove_button_locator)

            # Wait for the product row to disappear after clicking remove
            self.wait_for_element_to_disappear(remove_button_locator, timeout=10)
        except Exception as e:
            raise Exception(f"Failed to remove product '{product_name}' from the cart: {e}")

    def is_product_in_cart(self, product_name):
        product_locator = (By.XPATH, f"//tr[contains(., '{product_name}')]")
        return self.is_element_present(product_locator)

    def get_product_quantity(self, product_name):
        try:
            # Find the quantity field for the specific product
            quantity_locator = (By.XPATH, f"//td[@class='product-name']//a[text()='{product_name}']//following::input[1]")
            quantity_element = self.wait_for_element(quantity_locator)
            return int(quantity_element.get_attribute("value"))
        except Exception:
            return 0

    def get_cart_total_amount(self):
        try:
            # Get the total amount displayed in the cart
            total_amount_locator = (By.XPATH, "//tr[@class='order-total']//span[@class='woocommerce-Price-amount amount']")
            total_amount_element = self.wait_for_element(total_amount_locator)
            # Extract the amount as a float value (assuming the format is ₹123.45)
            total_amount_text = total_amount_element.text.replace("₹", "").strip()
            return float(total_amount_text)
        except Exception:
            return 0.0

    def wait_for_element_to_disappear(self, remove_button_locator):
        pass
