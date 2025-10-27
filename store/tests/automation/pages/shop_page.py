"""
Shop Page Object for automation testing
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class ShopPage(BasePage):
    """Page object for shop page"""
    
    # Locators
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".add-to-cart-btn")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CATEGORY_FILTER = (By.CSS_SELECTOR, "select[name='category']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "select[name='sort']")
    PAGINATION = (By.CSS_SELECTOR, ".pagination")
    NEXT_PAGE_LINK = (By.CSS_SELECTOR, ".pagination .next")
    PREV_PAGE_LINK = (By.CSS_SELECTOR, ".pagination .prev")
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon")
    CART_COUNT = (By.CSS_SELECTOR, ".cart-count")
    
    def __init__(self, driver, base_url="http://localhost:8000"):
        super().__init__(driver, base_url)
        self.url = "/shop/"
    
    def navigate_to_shop(self):
        """Navigate to shop page"""
        self.navigate_to(self.url)
    
    def get_product_cards(self):
        """
        Get all product cards
        
        Returns:
            list: List of product card elements
        """
        return self.find_elements(self.PRODUCT_CARDS)
    
    def get_product_count(self):
        """
        Get number of products displayed
        
        Returns:
            int: Number of products
        """
        return len(self.get_product_cards())
    
    def get_product_by_name(self, product_name):
        """
        Get product card by name
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            WebElement: Product card element or None
        """
        product_cards = self.get_product_cards()
        for card in product_cards:
            try:
                name_element = card.find_element(By.CSS_SELECTOR, ".product-name")
                if name_element.text.strip() == product_name:
                    return card
            except:
                continue
        return None
    
    def get_product_price(self, product_name):
        """
        Get product price by name
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            str: Product price or empty string
        """
        product_card = self.get_product_by_name(product_name)
        if product_card:
            try:
                price_element = product_card.find_element(By.CSS_SELECTOR, ".product-price")
                return price_element.text.strip()
            except:
                return ""
        return ""
    
    def add_product_to_cart(self, product_name):
        """
        Add product to cart by name
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            bool: True if successful
        """
        product_card = self.get_product_by_name(product_name)
        if product_card:
            try:
                add_button = product_card.find_element(By.CSS_SELECTOR, ".add-to-cart-btn")
                add_button.click()
                return True
            except:
                return False
        return False
    
    def search_products(self, search_term):
        """
        Search for products
        
        Args:
            search_term (str): Search term
        """
        self.send_keys_to_element(self.SEARCH_INPUT, search_term)
        self.click_element(self.SEARCH_BUTTON)
    
    def clear_search(self):
        """Clear search input"""
        search_input = self.find_element(self.SEARCH_INPUT)
        search_input.clear()
    
    def filter_by_category(self, category_name):
        """
        Filter products by category
        
        Args:
            category_name (str): Category name
        """
        category_select = Select(self.find_element(self.CATEGORY_FILTER))
        category_select.select_by_visible_text(category_name)
    
    def sort_products(self, sort_option):
        """
        Sort products by option
        
        Args:
            sort_option (str): Sort option (price_low, price_high, name, newest)
        """
        sort_select = Select(self.find_element(self.SORT_DROPDOWN))
        sort_select.select_by_value(sort_option)
    
    def get_sort_options(self):
        """
        Get available sort options
        
        Returns:
            list: List of sort option texts
        """
        sort_select = Select(self.find_element(self.SORT_DROPDOWN))
        return [option.text for option in sort_select.options]
    
    def get_categories(self):
        """
        Get available categories
        
        Returns:
            list: List of category names
        """
        category_select = Select(self.find_element(self.CATEGORY_FILTER))
        return [option.text for option in category_select.options if option.text != "All Categories"]
    
    def is_pagination_present(self):
        """
        Check if pagination is present
        
        Returns:
            bool: True if pagination is present
        """
        return self.is_element_present(self.PAGINATION)
    
    def go_to_next_page(self):
        """Go to next page"""
        if self.is_element_present(self.NEXT_PAGE_LINK):
            self.click_element(self.NEXT_PAGE_LINK)
            return True
        return False
    
    def go_to_previous_page(self):
        """Go to previous page"""
        if self.is_element_present(self.PREV_PAGE_LINK):
            self.click_element(self.PREV_PAGE_LINK)
            return True
        return False
    
    def get_cart_count(self):
        """
        Get cart item count
        
        Returns:
            int: Cart item count or 0
        """
        try:
            count_element = self.find_element(self.CART_COUNT)
            return int(count_element.text.strip())
        except:
            return 0
    
    def click_cart_icon(self):
        """Click cart icon"""
        self.click_element(self.CART_ICON)
    
    def is_product_available(self, product_name):
        """
        Check if product is available
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            bool: True if product is available
        """
        product_card = self.get_product_by_name(product_name)
        if product_card:
            try:
                # Check if "Out of Stock" label is present
                out_of_stock = product_card.find_elements(By.CSS_SELECTOR, ".out-of-stock")
                return len(out_of_stock) == 0
            except:
                return True
        return False
    
    def get_product_discount(self, product_name):
        """
        Get product discount percentage
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            str: Discount percentage or empty string
        """
        product_card = self.get_product_by_name(product_name)
        if product_card:
            try:
                discount_element = product_card.find_element(By.CSS_SELECTOR, ".discount")
                return discount_element.text.strip()
            except:
                return ""
        return ""
    
    def is_product_featured(self, product_name):
        """
        Check if product is featured
        
        Args:
            product_name (str): Name of the product
            
        Returns:
            bool: True if product is featured
        """
        product_card = self.get_product_by_name(product_name)
        if product_card:
            try:
                featured_badge = product_card.find_elements(By.CSS_SELECTOR, ".featured-badge")
                return len(featured_badge) > 0
            except:
                return False
        return False
    
    def get_all_product_names(self):
        """
        Get all product names on current page
        
        Returns:
            list: List of product names
        """
        product_cards = self.get_product_cards()
        names = []
        for card in product_cards:
            try:
                name_element = card.find_element(By.CSS_SELECTOR, ".product-name")
                names.append(name_element.text.strip())
            except:
                continue
        return names
    
    def get_all_product_prices(self):
        """
        Get all product prices on current page
        
        Returns:
            list: List of product prices
        """
        product_cards = self.get_product_cards()
        prices = []
        for card in product_cards:
            try:
                price_element = card.find_element(By.CSS_SELECTOR, ".product-price")
                prices.append(price_element.text.strip())
            except:
                continue
        return prices
