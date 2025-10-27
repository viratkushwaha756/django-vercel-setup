"""
Order Service - Handles order-related business logic
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import Cart, CartItem, Product


class OrderService:
    """Service class for order-related operations"""
    
    @staticmethod
    def create_order_from_cart(user, shipping_address=None, payment_method=None):
        """
        Create order from user's cart
        
        Args:
            user (User): User instance
            shipping_address (dict, optional): Shipping address
            payment_method (str, optional): Payment method
            
        Returns:
            dict: Order creation result
            
        Raises:
            ValidationError: If order creation fails
        """
        try:
            with transaction.atomic():
                cart = Cart.objects.get(user=user)
                cart_items = cart.items.all()
                
                if not cart_items.exists():
                    raise ValidationError("Cart is empty")
                
                # Validate cart items
                validation_results = OrderService._validate_cart_items(cart_items)
                if not validation_results['valid']:
                    raise ValidationError(f"Cart validation failed: {validation_results['issues']}")
                
                # Calculate order totals
                order_data = OrderService._calculate_order_totals(cart_items)
                
                # Create order (simplified - you would create an Order model)
                order_info = {
                    'user': user,
                    'items': cart_items,
                    'subtotal': order_data['subtotal'],
                    'tax': order_data['tax'],
                    'shipping': order_data['shipping'],
                    'total': order_data['total'],
                    'shipping_address': shipping_address,
                    'payment_method': payment_method,
                    'status': 'pending'
                }
                
                # Update product stock
                OrderService._update_product_stock(cart_items)
                
                # Clear cart after successful order
                cart.items.all().delete()
                
                return {
                    'success': True,
                    'order_info': order_info,
                    'message': 'Order created successfully'
                }
                
        except Exception as e:
            raise ValidationError(f"Failed to create order: {str(e)}")
    
    @staticmethod
    def _validate_cart_items(cart_items):
        """
        Validate cart items before order creation
        
        Args:
            cart_items (QuerySet): Cart items
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'valid': True,
            'issues': []
        }
        
        for item in cart_items:
            # Check if product is active
            if not item.product.is_active:
                validation_results['valid'] = False
                validation_results['issues'].append(
                    f"{item.product.name} is no longer available"
                )
                continue
            
            # Check stock availability
            if item.product.stock < item.quantity:
                validation_results['valid'] = False
                validation_results['issues'].append(
                    f"Only {item.product.stock} {item.product.name} available"
                )
        
        return validation_results
    
    @staticmethod
    def _calculate_order_totals(cart_items):
        """
        Calculate order totals
        
        Args:
            cart_items (QuerySet): Cart items
            
        Returns:
            dict: Order totals
        """
        subtotal = sum(item.total_price for item in cart_items)
        tax_rate = Decimal('0.08')  # 8% tax rate
        tax = subtotal * tax_rate
        shipping = Decimal('10.00') if subtotal < Decimal('50.00') else Decimal('0.00')
        total = subtotal + tax + shipping
        
        return {
            'subtotal': subtotal,
            'tax': tax,
            'shipping': shipping,
            'total': total
        }
    
    @staticmethod
    def _update_product_stock(cart_items):
        """
        Update product stock after order
        
        Args:
            cart_items (QuerySet): Cart items
        """
        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()
    
    @staticmethod
    def calculate_shipping_cost(subtotal):
        """
        Calculate shipping cost based on order total
        
        Args:
            subtotal (Decimal): Order subtotal
            
        Returns:
            Decimal: Shipping cost
        """
        if subtotal >= Decimal('50.00'):
            return Decimal('0.00')  # Free shipping over $50
        else:
            return Decimal('10.00')  # Standard shipping
    
    @staticmethod
    def calculate_tax(subtotal, tax_rate=0.08):
        """
        Calculate tax for order
        
        Args:
            subtotal (Decimal): Order subtotal
            tax_rate (float): Tax rate (default 8%)
            
        Returns:
            Decimal: Tax amount
        """
        return subtotal * Decimal(str(tax_rate))
    
    @staticmethod
    def get_order_summary(cart_items):
        """
        Get order summary information
        
        Args:
            cart_items (QuerySet): Cart items
            
        Returns:
            dict: Order summary
        """
        totals = OrderService._calculate_order_totals(cart_items)
        
        return {
            'items': cart_items,
            'item_count': cart_items.count(),
            'subtotal': totals['subtotal'],
            'tax': totals['tax'],
            'shipping': totals['shipping'],
            'total': totals['total']
        }
    
    @staticmethod
    def validate_payment_info(payment_data):
        """
        Validate payment information
        
        Args:
            payment_data (dict): Payment information
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'valid': True,
            'issues': []
        }
        
        required_fields = ['card_number', 'expiry_date', 'cvv', 'cardholder_name']
        
        for field in required_fields:
            if not payment_data.get(field):
                validation_results['valid'] = False
                validation_results['issues'].append(f"{field} is required")
        
        # Basic card number validation (simplified)
        if payment_data.get('card_number'):
            card_number = payment_data['card_number'].replace(' ', '').replace('-', '')
            if not card_number.isdigit() or len(card_number) < 13:
                validation_results['valid'] = False
                validation_results['issues'].append("Invalid card number")
        
        return validation_results
    
    @staticmethod
    def process_payment(order_info, payment_data):
        """
        Process payment for order (simplified implementation)
        
        Args:
            order_info (dict): Order information
            payment_data (dict): Payment data
            
        Returns:
            dict: Payment result
        """
        try:
            # Validate payment data
            validation = OrderService.validate_payment_info(payment_data)
            if not validation['valid']:
                return {
                    'success': False,
                    'message': f"Payment validation failed: {validation['issues']}"
                }
            
            # Simulate payment processing
            # In a real application, you would integrate with a payment gateway
            payment_result = {
                'success': True,
                'transaction_id': f"TXN_{order_info['user'].id}_{order_info['total']}",
                'message': 'Payment processed successfully'
            }
            
            return payment_result
            
        except Exception as e:
            return {
                'success': False,
                'message': f"Payment processing failed: {str(e)}"
            }
