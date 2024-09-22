from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

class ShopPage(BasePage):
    def __init__(self, driver, locators):
        super().__init__(driver)
        self.shop_link = (By.XPATH, locators['shop_page']['shop'])
        self.category_locators = {
            "android": (By.XPATH, locators['shop_page']['android_category']),
            "html": (By.XPATH, locators['shop_page']['html_category']),
            "javascript": (By.XPATH, locators['shop_page']['javascript_category']),
            "selenium": (By.XPATH, locators['shop_page']['selenium_category'])
        }
        # self.product_name = (By.XPATH, locators['shop_page']['product_name'])

    def go_to_shop(self):
        self.click_element(self.shop_link)

    def select_category(self, category_name):
        if category_name.lower() in self.category_locators:
            category_locator = self.category_locators[category_name.lower()]
            self.click_element(category_locator)
        else:
            raise ValueError(f"Category '{category_name}' not found in the category locators.")

    def verify_product_present(self, product_text):
        try:
            # Get the page source or visible text content
            page_content = self.driver.page_source

            # Normalize the text to make it case-insensitive and remove extra spaces
            normalized_page_content = page_content.lower().replace("\n", " ").strip()

            # Normalize the product text
            normalized_product_text = product_text.lower().strip()

            # Check if the product name is present in the page content
            return normalized_product_text in normalized_page_content
        except Exception:
            return False

    def add_product_to_basket(self, product_name):
        try:
            # Locate the "Add to Basket" button using the product name and click it
            add_to_basket_button = (By.XPATH, f"//h3[contains(text(), '{product_name}')]/following-sibling::div[@class='product_type_simple']/a[contains(@class, 'add_to_cart_button')]")
            self.click_element(add_to_basket_button)
        except Exception as e:
            raise Exception(f"Could not add product '{product_name}' to basket: {e}")

    def verify_product_details(self, product_name, product_details):
        try:
            # Locate the product details element using the product name
            product_details_locator = (By.XPATH, f"//h3[contains(text(), '{product_name}')]/following-sibling::div[contains(@class, 'product_description')]")
            product_details_element = self.wait_for_element(product_details_locator)
            # Check if the product details text matches the expected details
            return product_details.lower() in product_details_element.text.lower()
        except Exception as e:
            raise Exception(f"Could not verify product details for '{product_name}': {e}")

    def add_product_to_cart(self, product_name):
        try:
            # Locate the Add to Cart button based on the product name
            add_to_cart_locator = (
            By.XPATH, f"//li[contains(., '{product_name}')]//a[contains(@class, 'add_to_cart_button')]")

            # Scroll the element into view
            self.scroll_to_element(add_to_cart_locator)

            # Wait for the element to be clickable
            self.wait_for_clickable(add_to_cart_locator)

            # Attempt to click the element
            self.click_element(add_to_cart_locator)

        except ElementClickInterceptedException:
            # If click is intercepted, try using JavaScript to click the button
            self.click_element_using_js(add_to_cart_locator)

        except Exception as e:
            raise Exception(f"Failed to add product '{product_name}' to the cart: {e}")

    def scroll_to_product(self, product_name):
        """
        Scrolls the page to the specified product to make sure it's visible.
        """
        try:
            product_locator = (By.XPATH, f"//h3[contains(text(), '{product_name}')]")
            product_element = self.wait_for_element(product_locator)
            self.scroll_to_element(product_element)
        except Exception as e:
            print(f"Failed to scroll to product '{product_name}': {e}")

    def verify_product_present(self, product_text):
        try:
            # Check if the product name is partially present on the page
            product_elements = self.driver.find_elements(By.XPATH, f"//h3[contains(text(), '{product_text}')]")
            # If there is any element matching the product_text, return True
            return len(product_elements) > 0
        except Exception:
            return False
