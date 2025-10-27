"""
Base Page Object for automation testing
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Base page object class with common functionality"""
    
    def __init__(self, driver, base_url="http://localhost:8000"):
        """
        Initialize base page
        
        Args:
            driver: Selenium WebDriver instance
            base_url (str): Base URL of the application
        """
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL
        
        Args:
            url (str): URL to navigate to
        """
        full_url = f"{self.base_url}{url}" if url.startswith('/') else url
        self.driver.get(full_url)
    
    def find_element(self, locator):
        """
        Find element with explicit wait
        
        Args:
            locator (tuple): Element locator (By, value)
            
        Returns:
            WebElement: Found element
            
        Raises:
            TimeoutException: If element not found
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """
        Find multiple elements
        
        Args:
            locator (tuple): Element locator (By, value)
            
        Returns:
            list: List of found elements
        """
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator):
        """
        Click element with explicit wait
        
        Args:
            locator (tuple): Element locator (By, value)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        time.sleep(1)  # Small delay for UI updates
    
    def send_keys_to_element(self, locator, text):
        """
        Send keys to element
        
        Args:
            locator (tuple): Element locator (By, value)
            text (str): Text to send
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator):
        """
        Get text from element
        
        Args:
            locator (tuple): Element locator (By, value)
            
        Returns:
            str: Element text
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator):
        """
        Check if element is present
        
        Args:
            locator (tuple): Element locator (By, value)
            
        Returns:
            bool: True if element is present
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Element locator (By, value)
            
        Returns:
            bool: True if element is visible
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=10):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Element locator (By, value)
            timeout (int): Timeout in seconds
            
        Returns:
            WebElement: Visible element
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=10):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Element locator (By, value)
            timeout (int): Timeout in seconds
            
        Returns:
            WebElement: Clickable element
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def get_page_title(self):
        """
        Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def get_current_url(self):
        """
        Get current URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
    
    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
    
    def go_forward(self):
        """Go forward to next page"""
        self.driver.forward()
    
    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator (tuple): Element locator (By, value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def take_screenshot(self, filename):
        """
        Take screenshot for demonstration
        
        Args:
            filename (str): Screenshot filename
        """
        self.driver.save_screenshot(f"quality/{filename}.png")
        print(f"📸 Screenshot saved: quality/{filename}.png")
    
    def execute_javascript(self, script):
        """
        Execute JavaScript
        
        Args:
            script (str): JavaScript code to execute
            
        Returns:
            Any: JavaScript execution result
        """
        return self.driver.execute_script(script)
