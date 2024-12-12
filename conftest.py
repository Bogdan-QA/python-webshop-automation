import pytest
from selenium import webdriver
from pages.home_page import HomePage

def pytest_addoption(parser):
    """Add a command-line option for selecting the browser."""
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests: chrome or firefox"
    )

@pytest.fixture
def browser(request):
    """Initialize the selected browser."""
    browser_name = request.config.getoption("--browser")
    if browser_name == "chrome":
        driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    elif browser_name == "firefox":
        driver = webdriver.Firefox()  # Ensure geckodriver is in PATH
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def home_page(browser):
    """Fixture to initialize the HomePage and navigate to the website."""
    base_url = "https://demowebshop.tricentis.com/"  # Define the base URL here
    browser.get(base_url)  # Step 1: Open the website
    home_page = HomePage(browser)  # Step 2: Create HomePage object
    return home_page  # Return the HomePage object
