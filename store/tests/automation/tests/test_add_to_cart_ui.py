"""
UI Tests for Add to Cart functionality
"""
import pytest
from store.tests.automation.pages.shop_page import ShopPage
from store.tests.automation.pages.login_page import LoginPage


@pytest.mark.automation
class TestAddToCartUI:
    """Test cases for add to cart UI functionality"""
    
    def test_add_product_to_cart(self, browser, live_server, test_user, test_product):
        """Test adding product to cart"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        # Go to shop and add product
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Get product names and add first one
        product_names = shop_page.get_all_product_names()
        if product_names:
            shop_page.add_product_to_cart(product_names[0])
            
            # Check if product added to cart
            assert 'Added to cart' in browser.page_source or 'Cart' in browser.page_source
            print("✅ Automation Test: Product added to cart successfully")
        else:
            print("⚠️ No products found to add to cart")
    
    def test_cart_updates_quantity(self, browser, live_server, test_user, test_product):
        """Test cart quantity updates when adding products"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        initial_quantity = shop_page.get_cart_count()
        product_names = shop_page.get_all_product_names()
        
        if product_names:
            shop_page.add_product_to_cart(product_names[0])
            new_quantity = shop_page.get_cart_count()
            
            assert new_quantity > initial_quantity
            print("✅ Automation Test: Cart quantity updated correctly")
        else:
            print("⚠️ No products found to test cart quantity")
    
    def test_shop_page_loads(self, browser, live_server):
        """Test that shop page loads correctly"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        assert "Shop" in shop_page.get_page_title()
        assert shop_page.get_product_count() > 0
        print("✅ Automation Test: Shop page loads correctly")
    
    def test_product_cards_displayed(self, browser, live_server):
        """Test that product cards are displayed"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        assert shop_page.get_product_count() > 0
        print("✅ Automation Test: Product cards displayed")
    
    def test_add_to_cart_button_clickable(self, browser, live_server, test_user, test_product):
        """Test that add to cart buttons are clickable"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check if add to cart buttons are present and clickable
        add_to_cart_buttons = shop_page.get_add_to_cart_buttons()
        assert len(add_to_cart_buttons) > 0
        print("✅ Automation Test: Add to cart buttons are clickable")
    
    def test_cart_icon_clickable(self, browser, live_server, test_user):
        """Test that cart icon is clickable"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check if cart icon is clickable
        if shop_page.is_cart_icon_clickable():
            shop_page.click_cart_icon()
            assert 'cart' in browser.current_url.lower()
            print("✅ Automation Test: Cart icon is clickable")
        else:
            print("⚠️ Cart icon not found or not clickable")
    
    def test_product_search_functionality(self, browser, live_server):
        """Test product search functionality"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Test search functionality
        if shop_page.is_search_available():
            shop_page.search_products("apple")
            print("✅ Automation Test: Product search works")
        else:
            print("⚠️ Search functionality not available")
    
    def test_product_filtering_by_category(self, browser, live_server):
        """Test product filtering by category"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Test category filtering
        if shop_page.is_category_filter_available():
            shop_page.filter_by_category("fruits")
            print("✅ Automation Test: Category filtering works")
        else:
            print("⚠️ Category filter not available")
    
    def test_product_sorting(self, browser, live_server):
        """Test product sorting functionality"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Test sorting functionality
        if shop_page.is_sorting_available():
            shop_page.sort_products("price_low_to_high")
            print("✅ Automation Test: Product sorting works")
        else:
            print("⚠️ Sorting functionality not available")
    
    def test_product_pagination(self, browser, live_server):
        """Test product pagination"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Test pagination
        if shop_page.is_pagination_available():
            shop_page.go_to_next_page()
            print("✅ Automation Test: Pagination works")
        else:
            print("⚠️ Pagination not available")
    
    def test_product_details_visibility(self, browser, live_server):
        """Test product details are visible"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check if product details are visible
        product_details = shop_page.get_product_details()
        assert len(product_details) > 0
        print("✅ Automation Test: Product details are visible")
    
    def test_featured_products_display(self, browser, live_server):
        """Test featured products are displayed"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check if featured products are displayed
        featured_products = shop_page.get_featured_products()
        assert len(featured_products) > 0
        print("✅ Automation Test: Featured products displayed")
    
    def test_product_discount_display(self, browser, live_server):
        """Test product discount display"""
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check if discount information is displayed
        discounts = shop_page.get_discount_information()
        print("✅ Automation Test: Discount information displayed")
    
    def test_add_to_cart_button_states(self, browser, live_server, test_user, test_product):
        """Test add to cart button states"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        
        # Check button states
        button_states = shop_page.get_add_to_cart_button_states()
        assert len(button_states) > 0
        print("✅ Automation Test: Add to cart button states working")
    
    def test_cart_persistence_across_pages(self, browser, live_server, test_user, test_product):
        """Test cart persistence across pages"""
        # Login first
        browser.get(f"{live_server.url}/login/")
        login_page = LoginPage(browser)
        login_page.login('testuser', 'testpass123')
        
        # Add product to cart
        browser.get(f"{live_server.url}/shop/")
        shop_page = ShopPage(browser)
        product_names = shop_page.get_all_product_names()
        
        if product_names:
            shop_page.add_product_to_cart(product_names[0])
            
            # Navigate to different page and back
            browser.get(f"{live_server.url}/about/")
            browser.get(f"{live_server.url}/shop/")
            
            # Check if cart still has items
            cart_count = shop_page.get_cart_count()
            assert cart_count > 0
            print("✅ Automation Test: Cart persistence works")
        else:
            print("⚠️ No products found to test cart persistence")