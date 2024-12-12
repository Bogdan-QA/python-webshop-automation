from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.product_name = (By.CSS_SELECTOR, '.product-name')
        self.product_price = (By.CSS_SELECTOR, '.product-unit-price')
        self.product_qty = (By.CSS_SELECTOR, '.qty-input')
        self.remove_from_cart_checkbox = (By.CSS_SELECTOR, 'input[name="removefromcart"]')
        self.update_cart_btn = (By.CSS_SELECTOR, 'input[name="updatecart"]')
        self.order_summary_message = (By.CSS_SELECTOR, '.order-summary-content')
        self.terms_checkbox = (By.CSS_SELECTOR, '#termsofservice[type="checkbox"]')
        self.checkout_button = (By.XPATH, "//button[text()='Checkout']")

    # Method to retrieve product details from the cart
    def get_product_details(self):
        product_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.product_name)
        ).text
        product_price = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.product_price)
        ).text
        product_qty = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.product_qty)
        ).get_attribute("value")

        # Return the details as a dictionary
        return {
            "productTitle": product_title.strip(),
            "productPrice": product_price.strip(),
            "productQty": int(product_qty)
        }

    # Method to remove a product from the cart
    def remove_product_from_cart(self):
        remove_checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.remove_from_cart_checkbox)
        )
        remove_checkbox.click()

        update_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.update_cart_btn)
        )
        update_button.click()

    # Method to navigate to the checkout
    def navigate_to_checkout(self):
        terms_checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.terms_checkbox)
        )
        terms_checkbox.click()

        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_button)
        )
        checkout_button.click()
