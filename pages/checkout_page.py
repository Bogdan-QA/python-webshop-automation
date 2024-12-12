from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.country_dropdown = (By.ID, 'BillingNewAddress_CountryId')
        self.city_field = (By.ID, 'BillingNewAddress_City')
        self.address1_field = (By.ID, 'BillingNewAddress_Address1')
        self.zipcode_field = (By.ID, 'BillingNewAddress_ZipPostalCode')
        self.phone_field = (By.ID, 'BillingNewAddress_PhoneNumber')
        self.checkout_continue_button = (By.XPATH, "//button[text()='Continue']")
        self.shipping_method_continue_button = (By.CSS_SELECTOR, '#shipping-method-buttons-container [value="Continue"]')
        self.payment_method_continue_button = (By.CSS_SELECTOR, '#checkout-step-payment-method [value="Continue"]')
        self.payment_information_continue_button = (By.CSS_SELECTOR, '#checkout-step-payment-info [value="Continue"]')
        self.order_confirmation_continue_button = (By.CSS_SELECTOR, '#confirm-order-buttons-container [value="Confirm"]')
        self.order_successfully_processed_message = (By.XPATH, "//*[contains(text(), 'Your order has been')]")

    # Method to fill billing address mandatory fields
    def fill_billing_address_mandatory_fields(self, country, city, address1, zipcode, phone):
        # Select the country from the dropdown
        country_dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.country_dropdown)
        )
        Select(country_dropdown_element).select_by_visible_text(country)

        # Fill other fields
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.city_field)).send_keys(city)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.address1_field)).send_keys(address1)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.zipcode_field)).send_keys(zipcode)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_field)).send_keys(phone)

    # Method to confirm billing address
    def confirm_billing_address(self):
        self._click_continue_button()

    # Method to confirm shipping address
    def confirm_shipping_address(self):
        self._click_continue_button()

    # Method to confirm shipping method
    def confirm_shipping_method(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.shipping_method_continue_button)
        ).click()

    # Method to confirm payment method
    def confirm_payment_method(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_method_continue_button)
        ).click()

    # Method to confirm payment information
    def confirm_payment_information(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.payment_information_continue_button)
        ).click()

    # Method to confirm the order
    def confirm_order(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.order_confirmation_continue_button)
        ).click()

    # Method to get the order confirmation message
    def get_order_confirmation_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.order_successfully_processed_message)
        ).text

    # Private helper method to click a "Continue" button
    def _click_continue_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.checkout_continue_button)
        ).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located(self.checkout_continue_button))
