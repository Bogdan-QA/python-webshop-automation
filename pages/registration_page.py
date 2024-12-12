from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.gender_male = (By.ID, 'gender-male')
        self.gender_female = (By.ID, 'gender-female')
        self.first_name_field = (By.ID, 'FirstName')
        self.last_name_field = (By.ID, 'LastName')
        self.email_field = (By.ID, 'Email')
        self.password_field = (By.ID, 'Password')
        self.confirm_password_field = (By.ID, 'ConfirmPassword')
        self.register_button = (By.ID, 'register-button')
        self.registration_message = (By.CSS_SELECTOR, '.result')
        self.login_button = (By.CSS_SELECTOR, '.login-button')

    # Register a new user
    def register_user(self, first_name, last_name, email, password, confirm_password):
        """Registers a new user with the provided details."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_field)
        ).send_keys(first_name)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.last_name_field)
        ).send_keys(last_name)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)
        ).send_keys(email)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        ).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.confirm_password_field)
        ).send_keys(confirm_password)

        # Click the register button
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.register_button)
        ).click()

    # Log in as a user
    def login_user(self, email, password):
        """Logs in a user with the provided email and password."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)
        ).send_keys(email)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        ).send_keys(password)

        # Click the login button
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    # Get the registration message
    def get_registration_message(self):
        """Returns the registration success or error message."""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.registration_message)
        ).text
