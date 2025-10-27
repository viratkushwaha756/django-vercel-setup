"""
Login Page Object for automation testing
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for login page"""
    
    # Locators - Updated to match actual form fields
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger, .error")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    
    def __init__(self, driver, base_url="http://localhost:8000"):
        super().__init__(driver, base_url)
        self.url = "/accounts/login/"
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
    
    def enter_username(self, username):
        """
        Enter username
        
        Args:
            username (str): Username to enter
        """
        self.send_keys_to_element(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """
        Enter password
        
        Args:
            password (str): Password to enter
        """
        self.send_keys_to_element(self.PASSWORD_FIELD, password)
    
    def click_login_button(self):
        """Click login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """
        Perform complete login action
        
        Args:
            username (str): Username
            password (str): Password
        """
        print(f"🔧 Attempting login with: {username}")
        self.navigate_to_login()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.take_screenshot("after_login_attempt")
    
    def get_error_message(self):
        """
        Get error message text
        
        Returns:
            str: Error message text or empty string
        """
        try:
            return self.get_element_text(self.ERROR_MESSAGE)
        except:
            return "No error message found"
    
    def get_success_message(self):
        """
        Get success message text
        
        Returns:
            str: Success message text or empty string
        """
        try:
            return self.get_element_text(self.SUCCESS_MESSAGE)
        except:
            return ""
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error message is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed
        
        Returns:
            bool: True if success message is displayed
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def click_register_link(self):
        """Click register link"""
        self.click_element(self.REGISTER_LINK)
    
    def click_forgot_password_link(self):
        """Click forgot password link"""
        self.click_element(self.FORGOT_PASSWORD_LINK)
    
    def is_login_form_present(self):
        """
        Check if login form is present
        
        Returns:
            bool: True if login form is present
        """
        return (self.is_element_present(self.USERNAME_FIELD) and 
                self.is_element_present(self.PASSWORD_FIELD) and 
                self.is_element_present(self.LOGIN_BUTTON))
    
    def clear_login_form(self):
        """Clear login form fields"""
        username_field = self.find_element(self.USERNAME_FIELD)
        password_field = self.find_element(self.PASSWORD_FIELD)
        username_field.clear()
        password_field.clear()
    
    def is_logged_in(self):
        """
        Check if user is logged in (redirected from login page)
        
        Returns:
            bool: True if user is logged in
        """
        current_url = self.get_current_url()
        return self.url not in current_url
