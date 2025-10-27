"""
Unit tests for UserService
"""
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from store.services.user_service import UserService
from store.models import UserProfile


class TestUserService(TestCase):
    """Test cases for UserService"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user = UserService.create_user(**self.user_data)
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        
        # Check if profile was created
        self.assertTrue(hasattr(user, 'userprofile'))
    
    def test_create_user_duplicate_username(self):
        """Test user creation with duplicate username"""
        UserService.create_user(**self.user_data)
        
        with self.assertRaises(ValidationError):
            UserService.create_user(**self.user_data)
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        UserService.create_user(**self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        with self.assertRaises(ValidationError):
            UserService.create_user(**duplicate_data)
    
    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        UserService.create_user(**self.user_data)
        user = UserService.authenticate_user('testuser', 'testpass123')
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
    
    def test_authenticate_user_failure(self):
        """Test failed user authentication"""
        UserService.create_user(**self.user_data)
        user = UserService.authenticate_user('testuser', 'wrongpassword')
        
        self.assertIsNone(user)
    
    def test_get_user_profile_existing(self):
        """Test getting existing user profile"""
        user = UserService.create_user(**self.user_data)
        profile = UserService.get_user_profile(user)
        
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user, user)
    
    def test_get_user_profile_create_new(self):
        """Test creating new user profile"""
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='testpass123'
        )
        profile = UserService.get_user_profile(user)
        
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user, user)
    
    def test_update_user_profile(self):
        """Test updating user profile"""
        user = UserService.create_user(**self.user_data)
        profile = UserService.update_user_profile(
            user,
            phone='1234567890',
            address='123 Test St',
            city='Test City'
        )
        
        self.assertEqual(profile.phone, '1234567890')
        self.assertEqual(profile.address, '123 Test St')
        self.assertEqual(profile.city, 'Test City')
    
    def test_get_user_by_id_success(self):
        """Test getting user by ID"""
        user = UserService.create_user(**self.user_data)
        retrieved_user = UserService.get_user_by_id(user.id)
        
        self.assertEqual(retrieved_user, user)
    
    def test_get_user_by_id_not_found(self):
        """Test getting non-existent user by ID"""
        user = UserService.get_user_by_id(999)
        self.assertIsNone(user)
    
    def test_is_user_active(self):
        """Test checking if user is active"""
        user = UserService.create_user(**self.user_data)
        self.assertTrue(UserService.is_user_active(user))
        
        user.is_active = False
        user.save()
        self.assertFalse(UserService.is_user_active(user))
    
    def test_deactivate_user(self):
        """Test deactivating user"""
        user = UserService.create_user(**self.user_data)
        result = UserService.deactivate_user(user)
        
        self.assertTrue(result)
        user.refresh_from_db()
        self.assertFalse(user.is_active)
