"""
Checkout Page Object for automation testing
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for checkout page"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, ".cart-item-name")
    CART_ITEM_QUANTITIES = (By.CSS_SELECTOR, ".cart-item-quantity")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, ".cart-item-price")
    REMOVE_ITEM_BUTTONS = (By.CSS_SELECTOR, ".remove-item-btn")
    UPDATE_QUANTITY_INPUTS = (By.CSS_SELECTOR, ".quantity-input")
    UPDATE_QUANTITY_BUTTONS = (By.CSS_SELECTOR, ".update-quantity-btn")
    
    # Checkout form locators
    FIRST_NAME_FIELD = (By.ID, "id_first_name")
    LAST_NAME_FIELD = (By.ID, "id_last_name")
    EMAIL_FIELD = (By.ID, "id_email")
    PHONE_FIELD = (By.ID, "id_phone")
    ADDRESS_FIELD = (By.ID, "id_address")
    CITY_FIELD = (By.ID, "id_city")
    STATE_FIELD = (By.ID, "id_state")
    ZIP_CODE_FIELD = (By.ID, "id_zip_code")
    
    # Payment form locators
    CARD_NUMBER_FIELD = (By.ID, "id_card_number")
    EXPIRY_DATE_FIELD = (By.ID, "id_expiry_date")
    CVV_FIELD = (By.ID, "id_cvv")
    CARDHOLDER_NAME_FIELD = (By.ID, "id_cardholder_name")
    
    # Order summary locators
    SUBTOTAL = (By.CSS_SELECTOR, ".subtotal")
    TAX = (By.CSS_SELECTOR, ".tax")
    SHIPPING = (By.CSS_SELECTOR, ".shipping")
    TOTAL = (By.CSS_SELECTOR, ".total")
    
    # Action buttons
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, ".place-order-btn")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, ".continue-shopping-btn")
    CLEAR_CART_BUTTON = (By.CSS_SELECTOR, ".clear-cart-btn")
    
    # Messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    def __init__(self, driver, base_url="http://localhost:8000"):
        super().__init__(driver, base_url)
        self.url = "/cart/"
    
    def navigate_to_checkout(self):
        """Navigate to checkout page"""
        self.navigate_to(self.url)
    
    def get_cart_items(self):
        """
        Get all cart items
        
        Returns:
            list: List of cart item elements
        """
        return self.find_elements(self.CART_ITEMS)
    
    def get_cart_item_count(self):
        """
        Get number of items in cart
        
        Returns:
            int: Number of cart items
        """
        return len(self.get_cart_items())
    
    def get_cart_item_by_name(self, item_name):
        """
        Get cart item by name
        
        Args:
            item_name (str): Name of the item
            
        Returns:
            WebElement: Cart item element or None
        """
        cart_items = self.get_cart_items()
        for item in cart_items:
            try:
                name_element = item.find_element(By.CSS_SELECTOR, ".cart-item-name")
                if name_element.text.strip() == item_name:
                    return item
            except:
                continue
        return None
    
    def get_item_quantity(self, item_name):
        """
        Get item quantity by name
        
        Args:
            item_name (str): Name of the item
            
        Returns:
            int: Item quantity or 0
        """
        cart_item = self.get_cart_item_by_name(item_name)
        if cart_item:
            try:
                quantity_element = cart_item.find_element(By.CSS_SELECTOR, ".cart-item-quantity")
                return int(quantity_element.text.strip())
            except:
                return 0
        return 0
    
    def get_item_price(self, item_name):
        """
        Get item price by name
        
        Args:
            item_name (str): Name of the item
            
        Returns:
            str: Item price or empty string
        """
        cart_item = self.get_cart_item_by_name(item_name)
        if cart_item:
            try:
                price_element = cart_item.find_element(By.CSS_SELECTOR, ".cart-item-price")
                return price_element.text.strip()
            except:
                return ""
        return ""
    
    def update_item_quantity(self, item_name, new_quantity):
        """
        Update item quantity
        
        Args:
            item_name (str): Name of the item
            new_quantity (int): New quantity
            
        Returns:
            bool: True if successful
        """
        cart_item = self.get_cart_item_by_name(item_name)
        if cart_item:
            try:
                quantity_input = cart_item.find_element(By.CSS_SELECTOR, ".quantity-input")
                quantity_input.clear()
                quantity_input.send_keys(str(new_quantity))
                
                update_button = cart_item.find_element(By.CSS_SELECTOR, ".update-quantity-btn")
                update_button.click()
                return True
            except:
                return False
        return False
    
    def remove_item(self, item_name):
        """
        Remove item from cart
        
        Args:
            item_name (str): Name of the item
            
        Returns:
            bool: True if successful
        """
        cart_item = self.get_cart_item_by_name(item_name)
        if cart_item:
            try:
                remove_button = cart_item.find_element(By.CSS_SELECTOR, ".remove-item-btn")
                remove_button.click()
                return True
            except:
                return False
        return False
    
    def get_subtotal(self):
        """
        Get cart subtotal
        
        Returns:
            str: Subtotal amount
        """
        try:
            return self.get_element_text(self.SUBTOTAL)
        except:
            return ""
    
    def get_tax(self):
        """
        Get tax amount
        
        Returns:
            str: Tax amount
        """
        try:
            return self.get_element_text(self.TAX)
        except:
            return ""
    
    def get_shipping(self):
        """
        Get shipping amount
        
        Returns:
            str: Shipping amount
        """
        try:
            return self.get_element_text(self.SHIPPING)
        except:
            return ""
    
    def get_total(self):
        """
        Get total amount
        
        Returns:
            str: Total amount
        """
        try:
            return self.get_element_text(self.TOTAL)
        except:
            return ""
    
    def fill_shipping_info(self, first_name, last_name, email, phone, address, city, state, zip_code):
        """
        Fill shipping information
        
        Args:
            first_name (str): First name
            last_name (str): Last name
            email (str): Email address
            phone (str): Phone number
            address (str): Address
            city (str): City
            state (str): State
            zip_code (str): ZIP code
        """
        self.send_keys_to_element(self.FIRST_NAME_FIELD, first_name)
        self.send_keys_to_element(self.LAST_NAME_FIELD, last_name)
        self.send_keys_to_element(self.EMAIL_FIELD, email)
        self.send_keys_to_element(self.PHONE_FIELD, phone)
        self.send_keys_to_element(self.ADDRESS_FIELD, address)
        self.send_keys_to_element(self.CITY_FIELD, city)
        self.send_keys_to_element(self.STATE_FIELD, state)
        self.send_keys_to_element(self.ZIP_CODE_FIELD, zip_code)
    
    def fill_payment_info(self, card_number, expiry_date, cvv, cardholder_name):
        """
        Fill payment information
        
        Args:
            card_number (str): Card number
            expiry_date (str): Expiry date
            cvv (str): CVV
            cardholder_name (str): Cardholder name
        """
        self.send_keys_to_element(self.CARD_NUMBER_FIELD, card_number)
        self.send_keys_to_element(self.EXPIRY_DATE_FIELD, expiry_date)
        self.send_keys_to_element(self.CVV_FIELD, cvv)
        self.send_keys_to_element(self.CARDHOLDER_NAME_FIELD, cardholder_name)
    
    def place_order(self):
        """Place order"""
        self.click_element(self.PLACE_ORDER_BUTTON)
    
    def continue_shopping(self):
        """Continue shopping"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def clear_cart(self):
        """Clear cart"""
        self.click_element(self.CLEAR_CART_BUTTON)
    
    def get_success_message(self):
        """
        Get success message
        
        Returns:
            str: Success message text
        """
        try:
            return self.get_element_text(self.SUCCESS_MESSAGE)
        except:
            return ""
    
    def get_error_message(self):
        """
        Get error message
        
        Returns:
            str: Error message text
        """
        try:
            return self.get_element_text(self.ERROR_MESSAGE)
        except:
            return ""
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed
        
        Returns:
            bool: True if success message is displayed
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error message is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def is_cart_empty(self):
        """
        Check if cart is empty
        
        Returns:
            bool: True if cart is empty
        """
        return self.get_cart_item_count() == 0
    
    def get_all_item_names(self):
        """
        Get all item names in cart
        
        Returns:
            list: List of item names
        """
        cart_items = self.get_cart_items()
        names = []
        for item in cart_items:
            try:
                name_element = item.find_element(By.CSS_SELECTOR, ".cart-item-name")
                names.append(name_element.text.strip())
            except:
                continue
        return names
    
    def is_checkout_form_complete(self):
        """
        Check if checkout form is complete
        
        Returns:
            bool: True if form is complete
        """
        required_fields = [
            self.FIRST_NAME_FIELD,
            self.LAST_NAME_FIELD,
            self.EMAIL_FIELD,
            self.ADDRESS_FIELD,
            self.CITY_FIELD,
            self.STATE_FIELD,
            self.ZIP_CODE_FIELD,
            self.CARD_NUMBER_FIELD,
            self.EXPIRY_DATE_FIELD,
            self.CVV_FIELD,
            self.CARDHOLDER_NAME_FIELD
        ]
        
        for field in required_fields:
            try:
                element = self.find_element(field)
                if not element.get_attribute('value'):
                    return False
            except:
                return False
        
        return True
