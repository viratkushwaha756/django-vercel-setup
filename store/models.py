from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        """Get current price (sale price if available, otherwise regular price)"""
        try:
            if self.sale_price and self.sale_price > 0:
                return Decimal(str(self.sale_price))
            return Decimal(str(self.price))
        except (AttributeError, ValueError, TypeError):
            return Decimal('0.00')

    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        try:
            if self.sale_price and self.price > self.sale_price:
                price = Decimal(str(self.price))
                sale_price = Decimal(str(self.sale_price))
                discount = ((price - sale_price) / price) * Decimal('100')
                return int(discount)
            return 0
        except (AttributeError, ValueError, TypeError, ZeroDivisionError):
            return 0

    def get_image_url(self):
        """Return the product image URL or a static fallback"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        
        # Map products to specific images based on their name and category
        image_mapping = {
            # Fresh Fruits
            'Fresh Apples': '/static/img/fruite-item-1.jpg',
            'Organic Oranges': '/static/img/fruite-item-2.jpg',
            'Fresh Bananas': '/static/img/fruite-item-3.jpg',
            'Sweet Grapes': '/static/img/fruite-item-4.jpg',
            'Fresh Strawberries': '/static/img/fruite-item-5.jpg',
            'Ripe Mangoes': '/static/img/fruite-item-6.jpg',
            
            # Fresh Vegetables
            'Fresh Tomatoes': '/static/img/vegetable-item-1.jpg',
            'Organic Carrots': '/static/img/vegetable-item-2.jpg',
            'Green Broccoli': '/static/img/vegetable-item-3.png',
            'Fresh Spinach': '/static/img/vegetable-item-4.jpg',
            'Bell Peppers': '/static/img/vegetable-item-5.jpg',
            'Fresh Cucumbers': '/static/img/vegetable-item-6.jpg',
            
            # Exotic Fruits
            'Dragon Fruit': '/static/img/best-product-1.jpg',
            'Pomegranate': '/static/img/best-product-2.jpg',
            'Kiwi Fruits': '/static/img/best-product-3.jpg',
            'Fresh Pineapple': '/static/img/best-product-4.jpg',
            'Avocado': '/static/img/best-product-5.jpg',
            'Fresh Papaya': '/static/img/best-product-6.jpg',
        }
        
        return image_mapping.get(self.name, '/static/img/best-product-1.jpg')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.alt_text}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating} stars"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        """Calculate total cart price"""
        try:
            total = Decimal('0.00')
            for item in self.items.all():
                item_price = Decimal(str(item.product.current_price))
                item_quantity = Decimal(str(item.quantity))
                total += item_price * item_quantity
            return total
        except (AttributeError, ValueError, TypeError):
            return Decimal('0.00')
    
    @property
    def tax_amount(self):
        """Calculate 8% tax on subtotal"""
        try:
            tax_rate = Decimal('0.08')
            return self.total_price * tax_rate
        except (TypeError, AttributeError):
            return Decimal('0.00')
    
    @property
    def shipping_cost(self):
        """Calculate shipping cost (free if order >= $50)"""
        try:
            if self.total_price >= Decimal('50.00'):
                return Decimal('0.00')
            return Decimal('10.00')
        except (TypeError, AttributeError):
            return Decimal('10.00')
    
    @property
    def final_total(self):
        """Calculate final total including tax and shipping"""
        try:
            return self.total_price + self.tax_amount + self.shipping_cost
        except (TypeError, AttributeError):
            return Decimal('0.00')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        """Calculate item total price"""
        try:
            price = Decimal(str(self.product.current_price))
            quantity = Decimal(str(self.quantity))
            return price * quantity
        except (AttributeError, ValueError, TypeError):
            return Decimal('0.00')
