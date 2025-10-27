"""
Cart Service - Handles cart-related business logic
"""
from django.core.exceptions import ValidationError
from ..models import Cart, CartItem, Product


class CartService:
    """Service class for cart-related operations"""
    
    @staticmethod
    def get_or_create_cart(user):
        """
        Get or create cart for user
        
        Args:
            user (User): User instance
            
        Returns:
            Cart: User's cart
        """
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    
    @staticmethod
    def add_to_cart(user, product, quantity=1):
        """
        Add product to cart
        
        Args:
            user (User): User instance
            product (Product): Product instance
            quantity (int): Quantity to add
            
        Returns:
            CartItem: Created or updated cart item
            
        Raises:
            ValidationError: If operation fails
        """
        try:
            cart = CartService.get_or_create_cart(user)
            
            # Check if product is in stock
            if product.stock < quantity:
                raise ValidationError(f"Only {product.stock} items available in stock")
            
            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Update quantity if item already exists
                cart_item.quantity += quantity
                cart_item.save()
            
            return cart_item
            
        except Exception as e:
            raise ValidationError(f"Failed to add to cart: {str(e)}")
    
    @staticmethod
    def update_cart_item(user, product, quantity):
        """
        Update cart item quantity
        
        Args:
            user (User): User instance
            product (Product): Product instance
            quantity (int): New quantity
            
        Returns:
            CartItem: Updated cart item
            
        Raises:
            ValidationError: If operation fails
        """
        try:
            cart = CartService.get_or_create_cart(user)
            
            if quantity <= 0:
                # Remove item if quantity is 0 or negative
                CartService.remove_from_cart(user, product)
                return None
            
            # Check stock availability
            if product.stock < quantity:
                raise ValidationError(f"Only {product.stock} items available in stock")
            
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            
            return cart_item
            
        except CartItem.DoesNotExist:
            raise ValidationError("Item not found in cart")
        except Exception as e:
            raise ValidationError(f"Failed to update cart: {str(e)}")
    
    @staticmethod
    def remove_from_cart(user, product):
        """
        Remove product from cart
        
        Args:
            user (User): User instance
            product (Product): Product instance
            
        Returns:
            bool: True if successful
        """
        try:
            cart = CartService.get_or_create_cart(user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return True
            
        except CartItem.DoesNotExist:
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_cart_items(user):
        """
        Get all cart items for user
        
        Args:
            user (User): User instance
            
        Returns:
            QuerySet: Cart items
        """
        cart = CartService.get_or_create_cart(user)
        return cart.items.all()
    
    @staticmethod
    def get_cart_total(user):
        """
        Get cart total price
        
        Args:
            user (User): User instance
            
        Returns:
            float: Total cart price
        """
        cart = CartService.get_or_create_cart(user)
        return cart.total_price
    
    @staticmethod
    def get_cart_item_count(user):
        """
        Get total number of items in cart
        
        Args:
            user (User): User instance
            
        Returns:
            int: Total item count
        """
        cart = CartService.get_or_create_cart(user)
        return cart.total_items
    
    @staticmethod
    def clear_cart(user):
        """
        Clear all items from cart
        
        Args:
            user (User): User instance
            
        Returns:
            bool: True if successful
        """
        try:
            cart = CartService.get_or_create_cart(user)
            cart.items.all().delete()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_cart_summary(user):
        """
        Get cart summary information
        
        Args:
            user (User): User instance
            
        Returns:
            dict: Cart summary
        """
        cart = CartService.get_or_create_cart(user)
        items = cart.items.all()
        
        return {
            'cart': cart,
            'items': items,
            'total_items': cart.total_items,
            'total_price': cart.total_price,
            'item_count': items.count()
        }
    
    @staticmethod
    def validate_cart_items(user):
        """
        Validate cart items (check stock, availability)
        
        Args:
            user (User): User instance
            
        Returns:
            dict: Validation results
        """
        cart = CartService.get_or_create_cart(user)
        items = cart.items.all()
        
        validation_results = {
            'valid': True,
            'issues': [],
            'updated_items': []
        }
        
        for item in items:
            # Check if product is still active
            if not item.product.is_active:
                validation_results['issues'].append(
                    f"{item.product.name} is no longer available"
                )
                validation_results['valid'] = False
                continue
            
            # Check stock availability
            if item.product.stock < item.quantity:
                if item.product.stock == 0:
                    validation_results['issues'].append(
                        f"{item.product.name} is out of stock"
                    )
                    validation_results['valid'] = False
                else:
                    # Update quantity to available stock
                    validation_results['issues'].append(
                        f"{item.product.name} quantity reduced from {item.quantity} to {item.product.stock} (insufficient stock)"
                    )
                    item.quantity = item.product.stock
                    item.save()
                    validation_results['updated_items'].append(
                        f"{item.product.name} quantity updated to {item.product.stock}"
                    )
                    validation_results['valid'] = False  # Mark as invalid due to stock adjustment
        
        return validation_results
