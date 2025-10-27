"""
Shared fixtures for all tests
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():
    """Shared browser fixture for all automation tests"""
    chrome_options = Options()
    # Browser will be visible (not headless) for demonstration
    # chrome_options.add_argument("--headless")  # COMMENTED OUT FOR VISIBLE BROWSER
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    driver.quit()


@pytest.fixture
def live_server_url(live_server):
    """Helper fixture to get live server URL"""
    return live_server.url


@pytest.fixture
def test_user(django_user_model):
    """Create a test user for automation tests"""
    user = django_user_model.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )
    return user


@pytest.fixture
def test_product():
    """Create test products for automation tests"""
    from store.models import Category, Product
    
    # Create test category
    category = Category.objects.create(
        name='Test Category',
        slug='test-category',
        description='Test category for automation'
    )
    
    # Create test products
    products = []
    for i in range(5):
        product = Product.objects.create(
            name=f'Test Product {i+1}',
            slug=f'test-product-{i+1}',
            category=category,
            description=f'Test product {i+1} description',
            price=10.00 + (i * 5),
            stock=100,
            is_active=True
        )
        products.append(product)
    
    return products
