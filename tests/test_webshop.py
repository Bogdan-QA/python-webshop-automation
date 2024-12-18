import pytest
import json
import time

from selenium.webdriver.support.wait import WebDriverWait

from pages.home_page import HomePage
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegistrationPage
from pages.product_list_page import ProductListPage
from pages.cart_page import CartPage

from pages.checkout_page import CheckoutPage

# Load test data from JSON file
with open('test_data.json', 'r') as file:
    test_data = json.load(file)

@pytest.mark.parametrize("registration_data", [test_data["demoWebShopData"]["registrationData"]])
def test_verify_user_registration(browser, registration_data):
    """
    Verify that the application allows registering a user successfully.
    """
    # Initialize pages
    home_page = HomePage(browser)
    registration_page = RegistrationPage(browser)

    # Navigate to the home page and click the register link
    home_page.open()
    register_link = browser.find_element(*home_page.register_user)
    register_link.click()

    # Register the user
    registration_page.register_user(
        first_name=registration_data["firstName"],
        last_name=registration_data["lastName"],
        email=registration_data["email"],
        password=registration_data["password"],
        confirm_password=registration_data["confirmPassword"]
    )

    # Verify the registration message is visible
    registration_message = browser.find_element(*registration_page.registration_message)
    assert registration_message.is_displayed(), "Registration message is not visible"

    # Get and verify the registration message content
    actual_message = registration_page.get_registration_message()
    expected_message = test_data["demoWebShopData"]["successfulRegistrationMessage"]
    assert expected_message in actual_message, f"Expected '{expected_message}' but got '{actual_message}'"

@pytest.mark.parametrize("login_data", [test_data["demoWebShopData"]["loginData"]])
def test_verify_user_login(browser, login_data):
    """
    Verify that the application allows a user to log in successfully.
    """
    # Initialize pages
    home_page = HomePage(browser)
    registration_page = RegistrationPage(browser)

    # Navigate to the home page and click the login link
    home_page.open()
    login_link = browser.find_element(*home_page.login_user)
    login_link.click()

    # Log in the user
    registration_page.login_user(
        email=login_data["email"],
        password=login_data["password"]
    )

    # Get and verify the account email displayed
    actual_email = home_page.get_account_email()
    expected_email = login_data["email"]
    assert expected_email in actual_email, f"Expected '{expected_email}' but got '{actual_email}'"

@pytest.mark.parametrize("sub_category_titles", [test_data["demoWebShopData"]["subCategoryTitles"]])
def test_verify_computer_sub_groups(browser, sub_category_titles):
    """
    Verify that the Computers group has 3 subgroups with the correct names.
    """
    # Initialize pages
    home_page = HomePage(browser)
    product_list_page = ProductListPage(browser)

    # Navigate to the home page and click the Computers group link
    home_page.open()
    computers_group = browser.find_element(*home_page.computers_group)
    computers_group.click()

    # Verify the subcategory titles
    product_list_page.verify_sub_category_titles(expected_titles=sub_category_titles)

def test_verify_sort_products_by_price(browser):
    """
    Verify that the customer can sort products by price in ascending order.
    """
    # Initialize pages
    home_page = HomePage(browser)
    product_list_page = ProductListPage(browser)

    # Navigate to the home page and click the Books group link
    home_page.open()
    books_group = browser.find_element(*home_page.books_group)
    books_group.click()

    # Verify the products are sorted by price in ascending order
    product_list_page.verify_sort_by_price()

def test_verify_change_number_of_items_on_page(browser):
    """
    Verify that the customer can change the number of items displayed on the page.
    """
    # Initialize pages
    home_page = HomePage(browser)
    product_list_page = ProductListPage(browser)

    # Navigate to the home page and click the Books group link
    home_page.open()
    books_group = browser.find_element(*home_page.books_group)
    books_group.click()

    # Verify that the number of items can be changed
    product_list_page.change_number_of_items()

def test_verify_add_product_to_wishlist(browser):
    """
    Verify that the customer can add a product to the wishlist.
    """
    # Initialize pages
    home_page = HomePage(browser)
    product_list_page = ProductListPage(browser)

    # Navigate to the home page and click the Books group link
    home_page.open()
    books_group = browser.find_element(*home_page.books_group)
    books_group.click()

    # Verify that the wishlist button is visible
    wishlist_button = browser.find_element(*home_page.wishlist_button)
    assert wishlist_button.is_displayed(), "Wishlist button is not visible"

    # Check the initial number of items in the wishlist
    wishlist_quantity_text = browser.find_element(*home_page.wishlist_quantity).text
    initial_wishlist_count = int(''.join(filter(str.isdigit, wishlist_quantity_text)))
    assert initial_wishlist_count == 0, f"Expected 0 items in the wishlist, but found {initial_wishlist_count}"

    # Add a product to the wishlist
    product_list_page.add_product_to_wishlist()

    # Verify the number of items in the wishlist after adding a product
    wishlist_quantity_text_after = browser.find_element(*home_page.wishlist_quantity).text
    updated_wishlist_count = int(''.join(filter(str.isdigit, wishlist_quantity_text_after)))
    assert updated_wishlist_count == 1, f"Expected 1 item in the wishlist, but found {updated_wishlist_count}"

def test_verify_add_product_to_cart(browser):
    """
    Verify that the customer can add a product to the cart.
    """
    # Initialize pages
    home_page = HomePage(browser)
    product_list_page = ProductListPage(browser)
    cart_page = CartPage(browser)

    # Step 1: Navigate to the homepage and click the Books group
    home_page.open()
    books_group = browser.find_element(*home_page.books_group)
    books_group.click()

    # Step 2: Verify the cart button is visible
    cart_button = browser.find_element(*home_page.cart_button)
    assert cart_button.is_displayed(), "Cart button is not visible"

    # Step 3: Verify the initial cart count is 0
    initial_cart_text = browser.find_element(*home_page.cart_quantity).text
    initial_cart_count = int(''.join(filter(str.isdigit, initial_cart_text)))
    assert initial_cart_count == 0, f"Expected 0 items in the cart, but found {initial_cart_count}"

    # Step 4: Add a product to the cart
    added_product_details = product_list_page.add_product_to_cart()

    # Step 5: Wait until the cart quantity updates to 1
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element(home_page.cart_quantity, "1")
    )

    # Verify cart count is updated
    cart_quantity_text_after = browser.find_element(*home_page.cart_quantity).text
    updated_cart_count = int(''.join(filter(str.isdigit, cart_quantity_text_after)))
    assert updated_cart_count == 1, f"Expected 1 item in the cart, but found {updated_cart_count}"

    # Step 6: Click the cart button to navigate to the cart page
    cart_button.click()

    # Step 7: Retrieve product details from the cart
    product_details_in_cart = cart_page.get_product_details()

    # Step 8: Compare the product details with the added product
    assert product_details_in_cart["productTitle"] == added_product_details["productTitle"], \
        f"Expected product title '{added_product_details['productTitle']}' but got '{product_details_in_cart['productTitle']}'"
    assert product_details_in_cart["productPrice"] == added_product_details["actualPrice"], \
        f"Expected product price '{added_product_details['actualPrice']}' but got '{product_details_in_cart['productPrice']}'"
    assert product_details_in_cart["productQty"] == 1, \
        f"Expected product quantity '1' but got '{product_details_in_cart['productQty']}'"