from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
import time


class ProductListPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.sub_category_grid = (By.CSS_SELECTOR, '.sub-category-grid')
        self.sub_category_items = (By.CSS_SELECTOR, '.sub-category-grid .sub-category-item')
        self.sort_by_dropdown = (By.ID, 'products-orderby')
        self.product_grid = (By.CSS_SELECTOR, '.product-grid')
        self.product_items = (By.CSS_SELECTOR, '.product-grid .item-box')
        self.product_list_number = (By.ID, 'products-pagesize')
        self.product_item = (By.CSS_SELECTOR, '.product-item')
        self.product_title = (By.CSS_SELECTOR, '.product-title a')
        self.product_actual_price = (By.CSS_SELECTOR, '.actual-price')
        self.add_to_cart = (By.CSS_SELECTOR, '.button-2.product-box-add-to-cart-button')
        self.add_to_wishlist_btn = (By.CSS_SELECTOR, '.add-to-wishlist-button')
        self.fiction_ex_book = (By.CSS_SELECTOR, 'a[href="/fiction-ex"]')

    # Verify subcategory titles
    def verify_sub_category_titles(self, expected_titles):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.sub_category_grid)
        )

        # Verify there are exactly 3 items
        sub_category_items = self.driver.find_elements(*self.sub_category_items)
        assert len(sub_category_items) == 3, f"Expected 3 subcategories, but found {len(sub_category_items)}"

        # Collect titles and verify they match the expected titles
        actual_titles = [
            item.find_element(By.CSS_SELECTOR, '.title a').text.strip()
            for item in sub_category_items
        ]
        assert actual_titles == expected_titles, f"Expected titles {expected_titles}, but got {actual_titles}"

    # Verify sort by price (low to high)
    def verify_sort_by_price(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.sort_by_dropdown)
        )
        Select(dropdown).select_by_visible_text('Price: Low to High')

        # Wait for the sorting to complete
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.product_items)
        )

        # Collect all the actual prices
        product_items = self.driver.find_elements(*self.product_items)
        prices = [
            float(item.find_element(By.CSS_SELECTOR, '.actual-price').text.replace('$', '').strip())
            for item in product_items
        ]

        # Verify prices are sorted in ascending order
        assert prices == sorted(prices), f"Prices are not sorted correctly: {prices}"

    # Change the number of items displayed
    def change_number_of_items(self):
        initial_item_count = len(self.driver.find_elements(*self.product_items))
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.product_list_number)
        )
        Select(dropdown).select_by_visible_text('4')

        # Wait for the product grid to update
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.product_items)
        )

        current_item_count = len(self.driver.find_elements(*self.product_items))
        assert initial_item_count != current_item_count, "Item count did not change"
        assert current_item_count == 4, f"Expected 4 items, but got {current_item_count}"

    # Add the first product to the cart
    def add_product_to_cart(self):
        first_product = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.product_items)
        )[0]

        # Extract product details
        product_id = first_product.find_element(*self.product_item).get_attribute('data-productid')
        product_title = first_product.find_element(*self.product_title).text.strip()
        actual_price = first_product.find_element(*self.product_actual_price).text.strip()

        # Click "Add to cart"
        first_product.find_element(*self.add_to_cart).click()
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element(first_product.find_element(*self.add_to_cart))
        )

        return {
            "productId": product_id,
            "productTitle": product_title,
            "actualPrice": actual_price
        }

    # Add a specific product to the wishlist
    def add_product_to_wishlist(self):
        """Adds a specific product to the wishlist and returns product details."""
        # Re-find the fiction_ex_book element to ensure it is fresh
        fiction_ex_book = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.fiction_ex_book)
        )
        fiction_ex_book.click()

        # Locate the "Add to Wishlist" button
        wishlist_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_to_wishlist_btn)
        )

        # Scroll the button into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", wishlist_button)

        # Try clicking the button using JavaScript
        self.driver.execute_script("arguments[0].click();", wishlist_button)
        print("Debug: Wishlist button clicked using JavaScript.")

        # Wait for the wishlist count to update
        WebDriverWait(self.driver, 10).until(
            lambda driver: int(''.join(
                filter(str.isdigit, driver.find_element(By.CSS_SELECTOR, '.ico-wishlist .wishlist-qty').text))) > 0
        )

        # Re-query the product box to avoid stale element reference
        product_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.product_item)
        )

        # Extract product details
        product_id = product_box.get_attribute('data-productid')
        product_title = product_box.find_element(*self.product_title).text.strip()
        actual_price = product_box.find_element(*self.product_actual_price).text.strip()

        return {
            "productId": product_id,
            "productTitle": product_title,
            "actualPrice": actual_price
        }

    # Validate a book is in the wishlist
    def validate_book_in_wishlist(self, expected_book_title):
        book_title_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'td.product a'))
        )
        actual_book_title = book_title_element.text.strip()
        assert actual_book_title == expected_book_title, \
            f"Expected book title '{expected_book_title}', but got '{actual_book_title}'"
