"""
User Service - Handles user-related business logic
"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import UserProfile


class UserService:
    """Service class for user-related operations"""
    
    @staticmethod
    def create_user(username, email, password, first_name=None, last_name=None):
        """
        Create a new user with profile
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password
            first_name (str, optional): First name
            last_name (str, optional): Last name
            
        Returns:
            User: Created user instance
            
        Raises:
            ValidationError: If user creation fails
        """
        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    raise ValidationError("Username already exists")
                
                if User.objects.filter(email=email).exists():
                    raise ValidationError("Email already exists")
                
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name or '',
                    last_name=last_name or ''
                )
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
                return user
                
        except Exception as e:
            raise ValidationError(f"Failed to create user: {str(e)}")
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Authenticate user credentials
        
        Args:
            username (str): Username or email
            password (str): Password
            
        Returns:
            User: Authenticated user or None
        """
        return authenticate(username=username, password=password)
    
    @staticmethod
    def get_user_profile(user):
        """
        Get or create user profile
        
        Args:
            user (User): User instance
            
        Returns:
            UserProfile: User profile instance
        """
        try:
            return user.userprofile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=user)
    
    @staticmethod
    def update_user_profile(user, **kwargs):
        """
        Update user profile
        
        Args:
            user (User): User instance
            **kwargs: Profile fields to update
            
        Returns:
            UserProfile: Updated profile instance
        """
        try:
            profile = UserService.get_user_profile(user)
            
            # Update profile fields
            for field, value in kwargs.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)
            
            profile.save()
            return profile
            
        except Exception as e:
            raise ValidationError(f"Failed to update profile: {str(e)}")
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User instance or None
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def is_user_active(user):
        """
        Check if user is active
        
        Args:
            user (User): User instance
            
        Returns:
            bool: True if user is active
        """
        return user.is_active
    
    @staticmethod
    def deactivate_user(user):
        """
        Deactivate user account
        
        Args:
            user (User): User instance
            
        Returns:
            bool: True if successful
        """
        try:
            user.is_active = False
            user.save()
            return True
        except Exception:
            return False
