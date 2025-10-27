"""
Unit tests for CartService
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from store.services.cart_service import CartService
from store.models import Product, Category, Cart, CartItem


class TestCartService(TestCase):
    """Test cases for CartService"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
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
    
    def test_get_or_create_cart(self):
        """Test getting or creating cart"""
        cart = CartService.get_or_create_cart(self.user)
        
        self.assertIsInstance(cart, Cart)
        self.assertEqual(cart.user, self.user)
        
        # Test getting existing cart
        cart2 = CartService.get_or_create_cart(self.user)
        self.assertEqual(cart, cart2)
    
    def test_add_to_cart_success(self):
        """Test adding product to cart successfully"""
        cart_item = CartService.add_to_cart(self.user, self.product, 2)
        
        self.assertIsInstance(cart_item, CartItem)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.cart.user, self.user)
    
    def test_add_to_cart_existing_item(self):
        """Test adding existing product to cart"""
        # Add product first time
        CartService.add_to_cart(self.user, self.product, 2)
        
        # Add same product again
        cart_item = CartService.add_to_cart(self.user, self.product, 3)
        self.assertEqual(cart_item.quantity, 5)  # 2 + 3
    
    def test_add_to_cart_insufficient_stock(self):
        """Test adding product with insufficient stock"""
        with self.assertRaises(ValidationError):
            CartService.add_to_cart(self.user, self.product, 200)
    
    def test_update_cart_item_success(self):
        """Test updating cart item quantity"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        cart_item = CartService.update_cart_item(self.user, self.product, 5)
        
        self.assertEqual(cart_item.quantity, 5)
    
    def test_update_cart_item_remove(self):
        """Test removing cart item by setting quantity to 0"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        cart_item = CartService.update_cart_item(self.user, self.product, 0)
        
        self.assertIsNone(cart_item)
        self.assertFalse(CartItem.objects.filter(
            cart__user=self.user,
            product=self.product
        ).exists())
    
    def test_update_cart_item_not_found(self):
        """Test updating non-existent cart item"""
        with self.assertRaises(ValidationError):
            CartService.update_cart_item(self.user, self.product, 5)
    
    def test_remove_from_cart_success(self):
        """Test removing product from cart"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        result = CartService.remove_from_cart(self.user, self.product)
        
        self.assertTrue(result)
        self.assertFalse(CartItem.objects.filter(
            cart__user=self.user,
            product=self.product
        ).exists())
    
    def test_remove_from_cart_not_found(self):
        """Test removing non-existent cart item"""
        result = CartService.remove_from_cart(self.user, self.product)
        
        self.assertFalse(result)
    
    def test_get_cart_items(self):
        """Test getting cart items"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        cart_items = CartService.get_cart_items(self.user)
        
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().product, self.product)
        self.assertEqual(cart_items.first().quantity, 2)
    
    def test_get_cart_total(self):
        """Test getting cart total"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        total = CartService.get_cart_total(self.user)
        
        self.assertEqual(total, 20.00)  # 2 * 10.00
    
    def test_get_cart_item_count(self):
        """Test getting cart item count"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        count = CartService.get_cart_item_count(self.user)
        
        self.assertEqual(count, 2)
    
    def test_clear_cart(self):
        """Test clearing cart"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        result = CartService.clear_cart(self.user)
        
        self.assertTrue(result)
        self.assertEqual(CartService.get_cart_item_count(self.user), 0)
    
    def test_get_cart_summary(self):
        """Test getting cart summary"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        summary = CartService.get_cart_summary(self.user)
        
        self.assertIn('cart', summary)
        self.assertIn('items', summary)
        self.assertIn('total_items', summary)
        self.assertIn('total_price', summary)
        self.assertIn('item_count', summary)
        
        self.assertEqual(summary['total_items'], 2)
        self.assertEqual(summary['total_price'], 20.00)
        self.assertEqual(summary['item_count'], 1)
    
    def test_validate_cart_items_success(self):
        """Test validating cart items successfully"""
        CartService.add_to_cart(self.user, self.product, 2)
        
        validation = CartService.validate_cart_items(self.user)
        
        self.assertTrue(validation['valid'])
        self.assertEqual(len(validation['issues']), 0)
        self.assertEqual(len(validation['updated_items']), 0)
    
    def test_validate_cart_items_inactive_product(self):
        """Test validating cart with inactive product"""
        CartService.add_to_cart(self.user, self.product, 2)
        self.product.is_active = False
        self.product.save()
        
        validation = CartService.validate_cart_items(self.user)
        
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['issues']), 0)
    
    def test_validate_cart_items_insufficient_stock(self):
        """Test validating cart with insufficient stock"""
        CartService.add_to_cart(self.user, self.product, 2)
        self.product.stock = 1
        self.product.save()
        
        validation = CartService.validate_cart_items(self.user)
        
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['issues']), 0)
        self.assertGreater(len(validation['updated_items']), 0)
