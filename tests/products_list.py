import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.shop_page import ShopPage
from pages.cart_page import CartPage


@pytest.mark.usefixtures("setup", "config", "locators", "data")
class TestShop:

    @pytest.fixture(autouse=True)
    def class_fixtures(self, config, locators, data):
        """Assign fixtures to class attributes for use in tests."""
        self.config = config
        self.locators = locators
        self.data = data

    def capture_screenshot_on_failure(self, test_name):
        """Capture a screenshot in case of failure."""
        screenshot_name = f"screenshots/{test_name}.png"
        self.driver.save_screenshot(screenshot_name)
        print(f"Screenshot captured: {screenshot_name}")

    def register_user(self):
        """Reusable method to register a new user with unique email and password."""
        home_page = HomePage(self.driver, self.locators)
        registration_page = RegistrationPage(self.driver, self.locators)

        # Open the base URL and navigate to the My Account page
        self.driver.get(self.config['base_url'])
        home_page.go_to_my_account()

        # Register a new user with unique email and password
        new_email = self.data['registration']['email']
        new_password = self.data['registration']['password']
        registration_page.register(new_email, new_password)

        return new_email, new_password

    def verify_product_in_category(self, shop_page, product_name):
        """Helper method to verify the presence of a product in a category."""
        if not shop_page.verify_product_present(product_name):
            pytest.fail(f"Product '{product_name}' is not present in the selected category.")
        print(f"Product '{product_name}' is present in the selected category.")

    def test_case_16_verify_products_from_category(self):
        """
        Verify the presence of a product from the specified category.
        """
        try:
            # Register a new user
            self.register_user()

            # Navigate to Shop Page and select the category
            shop_page = ShopPage(self.driver, self.locators)
            shop_page.go_to_shop()
            shop_page.select_category(self.data['shop']['category'])

            # Verify the presence of the product in the selected category
            product_name = self.data['shop']['product_name']
            self.verify_product_in_category(shop_page, product_name)

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_16_verify_products_from_category")
            pytest.fail(f"Test Case 16 failed: {e}")

    def test_case_17_add_product_to_cart(self):
        """
        Verify the presence of a product and add it to the cart if present.
        """
        try:
            # Register a new user
            self.register_user()

            # Navigate to Shop Page and select the category
            shop_page = ShopPage(self.driver, self.locators)
            shop_page.go_to_shop()
            shop_page.select_category(self.data['shop']['category'])

            # Verify and add the product to the cart
            product_name = self.data['shop']['product_name']
            self.verify_product_in_category(shop_page, product_name)
            shop_page.add_product_to_cart(product_name)
            print(f"Product '{product_name}' added to the cart.")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_17_add_product_to_cart")
            pytest.fail(f"Test Case 17 failed: {e}")

    def test_case_18_add_multiple_products_to_cart(self):
        """
        Verify the presence of multiple products and add them to the cart if present.
        """
        try:
            # Register a new user
            self.register_user()

            # Navigate to Shop Page and select the category
            shop_page = ShopPage(self.driver, self.locators)
            shop_page.go_to_shop()
            shop_page.select_category(self.data['shop']['category'])

            # Verify and add each product to the cart
            product_names = self.data['shop']['product_names']
            for product_name in product_names:
                if shop_page.verify_product_present(product_name):
                    shop_page.add_product_to_cart(product_name)
                    print(f"Product '{product_name}' added to the cart.")
                else:
                    print(f"Product '{product_name}' is not present in the selected category.")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_18_add_multiple_products_to_cart")
            pytest.fail(f"Test Case 18 failed: {e}")

    def test_case_19_verify_products_in_cart(self):
        """
        Verify that the added products are present in the cart with the correct quantity.
        """
        try:
            # Register a new user
            self.register_user()

            # Navigate to Shop Page and add products to the cart
            shop_page = ShopPage(self.driver, self.locators)
            shop_page.go_to_shop()
            product_names = self.data['shop'].get('product_names', [])
            if not product_names:
                pytest.fail("No product names found in the 'shop' section of data.yaml.")

            for product_name in product_names:
                if shop_page.verify_product_present(product_name):
                    shop_page.add_product_to_cart(product_name)
                else:
                    print(f"Product '{product_name}' is not present in the selected category.")

            # Navigate to Cart and verify the products
            cart_page = CartPage(self.driver, self.locators)
            cart_page.go_to_cart()

            for product_name in product_names:
                assert cart_page.is_product_in_cart(product_name), \
                    f"Product '{product_name}' is not found in the cart."

            # Verify the quantity of each product
            for product_name in product_names:
                quantity = cart_page.get_product_quantity(product_name)
                assert quantity == 1, \
                    f"Expected quantity of product '{product_name}' is 1, but got '{quantity}'."

            # Print the total amount in the cart
            total_amount = cart_page.get_cart_total_amount()
            print(f"Total amount in the cart: ₹{total_amount}")

        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            self.capture_screenshot_on_failure("test_case_19_verify_products_in_cart")
            pytest.fail(f"Test Case 19 failed: {e}")
