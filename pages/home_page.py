from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.register_user = (By.CSS_SELECTOR, '.ico-register')
        self.login_user = (By.CSS_SELECTOR, '.ico-login')
        self.logged_in_account = (By.CSS_SELECTOR, '.account')
        self.top_navigation = (By.CSS_SELECTOR, '.top-menu')
        self.computers_group = (By.CSS_SELECTOR, '.top-menu a[href="/computers"]')
        self.books_group = (By.CSS_SELECTOR, '.top-menu a[href="/books"]')
        self.cart_button = (By.CSS_SELECTOR, '.ico-cart')
        self.cart_quantity = (By.CSS_SELECTOR, '.ico-cart .cart-qty')
        self.wishlist_button = (By.CSS_SELECTOR, '.ico-wishlist')
        self.wishlist_quantity = (By.CSS_SELECTOR, '.ico-wishlist .wishlist-qty')

    # Open the home page
    def open(self):
        """Navigates to the Demo Web Shop homepage."""
        base_url = "https://demowebshop.tricentis.com/"
        self.driver.get(base_url)

    # Get the account email of the logged-in user
    def get_account_email(self):
        """Returns the email of the logged-in user."""
        account_email_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.logged_in_account)
        )
        return account_email_element.text

    # Verify the subcategories under the Computers group
    def verify_computers_subcategories(self, expected_subcategories):
        """Verifies that the Computers subcategories match the expected list."""
        computers_group = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.computers_group)
        )
        computers_group.click()

        subcategories = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sub-category-item a'))
        )
        actual_subcategories = [subcategory.text for subcategory in subcategories]

        assert actual_subcategories == expected_subcategories, \
            f"Expected {expected_subcategories}, but got {actual_subcategories}"

    # Add an item to the wishlist
    def add_item_to_wishlist(self):
        """Clicks the wishlist button to add an item to the wishlist."""
        wishlist_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.wishlist_button)
        )
        wishlist_button.click()
