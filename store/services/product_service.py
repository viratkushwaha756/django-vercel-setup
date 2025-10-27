"""
Product Service - Handles product-related business logic
"""
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from ..models import Product, Category, Review


class ProductService:
    """Service class for product-related operations"""
    
    @staticmethod
    def get_all_products():
        """
        Get all active products
        
        Returns:
            QuerySet: All active products
        """
        return Product.objects.filter(is_active=True)
    
    @staticmethod
    def get_featured_products(limit=6):
        """
        Get featured products
        
        Args:
            limit (int): Maximum number of products to return
            
        Returns:
            QuerySet: Featured products
        """
        return Product.objects.filter(
            is_featured=True, 
            is_active=True
        )[:limit]
    
    @staticmethod
    def get_products_by_category(category_slug):
        """
        Get products by category
        
        Args:
            category_slug (str): Category slug
            
        Returns:
            QuerySet: Products in the category
        """
        return Product.objects.filter(
            category__slug=category_slug,
            is_active=True
        )
    
    @staticmethod
    def search_products(query):
        """
        Search products by name, description, or category
        
        Args:
            query (str): Search query
            
        Returns:
            QuerySet: Matching products
        """
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        )
    
    @staticmethod
    def get_product_by_slug(slug):
        """
        Get product by slug
        
        Args:
            slug (str): Product slug
            
        Returns:
            Product: Product instance or None
        """
        try:
            return Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return None
    
    @staticmethod
    def get_related_products(product, limit=4):
        """
        Get related products from the same category
        
        Args:
            product (Product): Product instance
            limit (int): Maximum number of related products
            
        Returns:
            QuerySet: Related products
        """
        return Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:limit]
    
    @staticmethod
    def get_products_paginated(products, page_number=1, per_page=12):
        """
        Get paginated products
        
        Args:
            products (QuerySet): Products queryset
            page_number (int): Page number
            per_page (int): Items per page
            
        Returns:
            Page: Paginated products
        """
        paginator = Paginator(products, per_page)
        return paginator.get_page(page_number)
    
    @staticmethod
    def sort_products(products, sort_by='newest'):
        """
        Sort products by specified criteria
        
        Args:
            products (QuerySet): Products queryset
            sort_by (str): Sort criteria
            
        Returns:
            QuerySet: Sorted products
        """
        if sort_by == 'price_low':
            return products.order_by('price')
        elif sort_by == 'price_high':
            return products.order_by('-price')
        elif sort_by == 'name':
            return products.order_by('name')
        elif sort_by == 'rating':
            return products.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')
        else:  # newest
            return products.order_by('-created_at')
    
    @staticmethod
    def get_product_reviews(product):
        """
        Get product reviews
        
        Args:
            product (Product): Product instance
            
        Returns:
            QuerySet: Product reviews
        """
        return product.reviews.all().order_by('-created_at')
    
    @staticmethod
    def get_product_rating(product):
        """
        Get average product rating
        
        Args:
            product (Product): Product instance
            
        Returns:
            float: Average rating or 0
        """
        reviews = product.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return 0
    
    @staticmethod
    def get_review_count(product):
        """
        Get total review count for product
        
        Args:
            product (Product): Product instance
            
        Returns:
            int: Review count
        """
        return product.reviews.count()
    
    @staticmethod
    def add_product_review(product, user, rating, comment):
        """
        Add review to product
        
        Args:
            product (Product): Product instance
            user (User): User instance
            rating (int): Rating (1-5)
            comment (str): Review comment
            
        Returns:
            Review: Created review instance
            
        Raises:
            ValidationError: If review creation fails
        """
        try:
            # Check if user already reviewed this product
            if Review.objects.filter(product=product, user=user).exists():
                raise ValidationError("You have already reviewed this product")
            
            review = Review.objects.create(
                product=product,
                user=user,
                rating=rating,
                comment=comment
            )
            return review
            
        except Exception as e:
            raise ValidationError(f"Failed to add review: {str(e)}")
    
    @staticmethod
    def get_categories():
        """
        Get all categories
        
        Returns:
            QuerySet: All categories
        """
        return Category.objects.all().order_by('name')
    
    @staticmethod
    def get_products_in_stock():
        """
        Get products that are in stock
        
        Returns:
            QuerySet: Products with stock > 0
        """
        return Product.objects.filter(
            is_active=True,
            stock__gt=0
        )
    
    @staticmethod
    def update_product_stock(product, quantity):
        """
        Update product stock
        
        Args:
            product (Product): Product instance
            quantity (int): Quantity to add/subtract
            
        Returns:
            bool: True if successful
        """
        try:
            new_stock = product.stock + quantity
            if new_stock < 0:
                product.stock = 0
            else:
                product.stock = new_stock
            product.save()
            return True
        except Exception:
            return False
