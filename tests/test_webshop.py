import pytest
import json
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.product_list_page import ProductListPage

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
