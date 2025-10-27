"""
Unit tests for ProductService
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from store.services.product_service import ProductService
from store.models import Product, Category, Review


class TestProductService(TestCase):
    """Test cases for ProductService"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test category description'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=10.00,
            stock=100,
            is_active=True
        )
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_get_all_products(self):
        """Test getting all active products"""
        products = ProductService.get_all_products()
        
        self.assertIn(self.product, products)
        self.assertEqual(products.count(), 1)
    
    def test_get_featured_products(self):
        """Test getting featured products"""
        self.product.is_featured = True
        self.product.save()
        
        featured_products = ProductService.get_featured_products()
        
        self.assertIn(self.product, featured_products)
        self.assertEqual(featured_products.count(), 1)
    
    def test_get_products_by_category(self):
        """Test getting products by category"""
        products = ProductService.get_products_by_category('test-category')
        
        self.assertIn(self.product, products)
        self.assertEqual(products.count(), 1)
    
    def test_search_products(self):
        """Test searching products"""
        # Search by name
        results = ProductService.search_products('Test Product')
        self.assertIn(self.product, results)
        
        # Search by description
        results = ProductService.search_products('description')
        self.assertIn(self.product, results)
        
        # Search by category
        results = ProductService.search_products('Test Category')
        self.assertIn(self.product, results)
    
    def test_get_product_by_slug(self):
        """Test getting product by slug"""
        product = ProductService.get_product_by_slug('test-product')
        
        self.assertEqual(product, self.product)
    
    def test_get_product_by_slug_not_found(self):
        """Test getting non-existent product by slug"""
        product = ProductService.get_product_by_slug('non-existent')
        self.assertIsNone(product)
    
    def test_get_related_products(self):
        """Test getting related products"""
        # Create another product in the same category
        related_product = Product.objects.create(
            name='Related Product',
            slug='related-product',
            category=self.category,
            description='Related product description',
            price=15.00,
            stock=50,
            is_active=True
        )
        
        related_products = ProductService.get_related_products(self.product)
        
        self.assertIn(related_product, related_products)
        self.assertNotIn(self.product, related_products)
    
    def test_sort_products(self):
        """Test sorting products"""
        # Create another product with different price
        Product.objects.create(
            name='Another Product',
            slug='another-product',
            category=self.category,
            description='Another product description',
            price=5.00,
            stock=50,
            is_active=True
        )
        
        products = Product.objects.filter(is_active=True)
        
        # Test price low to high
        sorted_products = ProductService.sort_products(products, 'price_low')
        self.assertEqual(sorted_products.first().price, 5.00)
        
        # Test price high to low
        sorted_products = ProductService.sort_products(products, 'price_high')
        self.assertEqual(sorted_products.first().price, 10.00)
        
        # Test by name
        sorted_products = ProductService.sort_products(products, 'name')
        self.assertEqual(sorted_products.first().name, 'Another Product')
    
    def test_add_product_review_success(self):
        """Test adding product review successfully"""
        review = ProductService.add_product_review(
            self.product,
            self.user,
            5,
            'Great product!'
        )
        
        self.assertIsInstance(review, Review)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product!')
    
    def test_add_product_review_duplicate(self):
        """Test adding duplicate review"""
        ProductService.add_product_review(
            self.product,
            self.user,
            5,
            'Great product!'
        )
        
        with self.assertRaises(ValidationError):
            ProductService.add_product_review(
                self.product,
                self.user,
                4,
                'Another review'
            )
    
    def test_get_product_rating(self):
        """Test getting product rating"""
        # Add some reviews
        ProductService.add_product_review(
            self.product,
            self.user,
            5,
            'Great product!'
        )
        
        # Create another user and review
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        ProductService.add_product_review(
            self.product,
            user2,
            3,
            'Average product'
        )
        
        rating = ProductService.get_product_rating(self.product)
        self.assertEqual(rating, 4.0)  # (5 + 3) / 2
    
    def test_get_review_count(self):
        """Test getting review count"""
        # Initially no reviews
        count = ProductService.get_review_count(self.product)
        self.assertEqual(count, 0)
        
        # Add a review
        ProductService.add_product_review(
            self.product,
            self.user,
            5,
            'Great product!'
        )
        
        count = ProductService.get_review_count(self.product)
        self.assertEqual(count, 1)
    
    def test_get_categories(self):
        """Test getting all categories"""
        categories = ProductService.get_categories()
        
        self.assertIn(self.category, categories)
        self.assertEqual(categories.count(), 1)
    
    def test_get_products_in_stock(self):
        """Test getting products in stock"""
        # Create out of stock product
        Product.objects.create(
            name='Out of Stock Product',
            slug='out-of-stock-product',
            category=self.category,
            description='Out of stock product description',
            price=20.00,
            stock=0,
            is_active=True
        )
        
        in_stock_products = ProductService.get_products_in_stock()
        
        self.assertIn(self.product, in_stock_products)
        self.assertEqual(in_stock_products.count(), 1)
    
    def test_update_product_stock(self):
        """Test updating product stock"""
        initial_stock = self.product.stock
        print(f"Initial stock: {initial_stock}")
        
        # Add stock
        result = ProductService.update_product_stock(self.product, 10)
        self.assertTrue(result)
        self.product.refresh_from_db()
        print(f"After +10: {self.product.stock}")
        self.assertEqual(self.product.stock, initial_stock + 10)
        
        # Remove stock
        result = ProductService.update_product_stock(self.product, -5)
        self.assertTrue(result)
        self.product.refresh_from_db()
        print(f"After -5: {self.product.stock}")
        self.assertEqual(self.product.stock, initial_stock + 5)
        
        # Try to remove more than available
        result = ProductService.update_product_stock(self.product, -100)        
        self.assertTrue(result)
        self.product.refresh_from_db()
        print(f"After -100: {self.product.stock}")
        self.assertEqual(self.product.stock, 5)  # 105 - 100 = 5
