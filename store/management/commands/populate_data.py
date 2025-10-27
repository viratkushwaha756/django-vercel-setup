from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Category, Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate database with sample products'

    def handle(self, *args, **options):
        # Create categories
        fruits_category, created = Category.objects.get_or_create(
            name='Fresh Fruits',
            defaults={
                'slug': 'fresh-fruits',
                'description': 'Fresh and organic fruits'
            }
        )
        
        vegetables_category, created = Category.objects.get_or_create(
            name='Fresh Vegetables',
            defaults={
                'slug': 'fresh-vegetables',
                'description': 'Fresh and organic vegetables'
            }
        )
        
        exotic_category, created = Category.objects.get_or_create(
            name='Exotic Fruits',
            defaults={
                'slug': 'exotic-fruits',
                'description': 'Exotic and rare fruits'
            }
        )

        # Sample products data
        products_data = [
            # Fruits
            {
                'name': 'Fresh Apples',
                'description': 'Sweet and juicy red apples',
                'price': 4.99,
                'category': fruits_category,
                'image_name': 'fruite-item-1.jpg'
            },
            {
                'name': 'Organic Oranges',
                'description': 'Vitamin C rich oranges',
                'price': 3.99,
                'category': fruits_category,
                'image_name': 'fruite-item-2.jpg'
            },
            {
                'name': 'Fresh Bananas',
                'description': 'Yellow ripe bananas',
                'price': 2.99,
                'category': fruits_category,
                'image_name': 'fruite-item-3.jpg'
            },
            {
                'name': 'Sweet Grapes',
                'description': 'Seedless green grapes',
                'price': 5.99,
                'category': fruits_category,
                'image_name': 'fruite-item-4.jpg'
            },
            {
                'name': 'Fresh Strawberries',
                'description': 'Red sweet strawberries',
                'price': 6.99,
                'category': fruits_category,
                'image_name': 'fruite-item-5.jpg'
            },
            {
                'name': 'Ripe Mangoes',
                'description': 'Sweet tropical mangoes',
                'price': 4.49,
                'category': fruits_category,
                'image_name': 'fruite-item-6.jpg'
            },
            
            # Vegetables
            {
                'name': 'Fresh Tomatoes',
                'description': 'Red ripe tomatoes - perfect for salads and cooking',
                'price': 2.99,
                'category': vegetables_category,
                'image_name': 'vegetable-item-1.jpg'
            },
            {
                'name': 'Organic Carrots',
                'description': 'Fresh orange carrots - rich in vitamins and minerals',
                'price': 1.99,
                'category': vegetables_category,
                'image_name': 'vegetable-item-2.jpg'
            },
            {
                'name': 'Green Broccoli',
                'description': 'Fresh green broccoli - packed with nutrients',
                'price': 3.49,
                'category': vegetables_category,
                'image_name': 'vegetable-item-3.png'
            },
            {
                'name': 'Fresh Spinach',
                'description': 'Organic spinach leaves - perfect for healthy meals',
                'price': 2.49,
                'category': vegetables_category,
                'image_name': 'vegetable-item-4.jpg'
            },
            {
                'name': 'Bell Peppers',
                'description': 'Colorful bell peppers - sweet and crunchy',
                'price': 3.99,
                'category': vegetables_category,
                'image_name': 'vegetable-item-5.jpg'
            },
            {
                'name': 'Fresh Cucumbers',
                'description': 'Crisp green cucumbers - refreshing and hydrating',
                'price': 1.49,
                'category': vegetables_category,
                'image_name': 'vegetable-item-6.jpg'
            },
            
            # Exotic Fruits
            {
                'name': 'Dragon Fruit',
                'description': 'Exotic dragon fruit',
                'price': 8.99,
                'category': exotic_category,
                'image_name': 'best-product-1.jpg'
            },
            {
                'name': 'Pomegranate',
                'description': 'Fresh pomegranate',
                'price': 5.99,
                'category': exotic_category,
                'image_name': 'best-product-2.jpg'
            },
            {
                'name': 'Kiwi Fruits',
                'description': 'Fresh kiwi fruits',
                'price': 4.99,
                'category': exotic_category,
                'image_name': 'best-product-3.jpg'
            },
            {
                'name': 'Fresh Pineapple',
                'description': 'Sweet pineapple',
                'price': 6.99,
                'category': exotic_category,
                'image_name': 'best-product-4.jpg'
            },
            {
                'name': 'Avocado',
                'description': 'Ripe avocados',
                'price': 3.99,
                'category': exotic_category,
                'image_name': 'best-product-5.jpg'
            },
            {
                'name': 'Fresh Papaya',
                'description': 'Sweet papaya',
                'price': 4.49,
                'category': exotic_category,
                'image_name': 'best-product-6.jpg'
            },
        ]

        # Create products
        for product_data in products_data:
            # Create slug from name
            slug = product_data['name'].lower().replace(' ', '-').replace('&', 'and')
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slug,
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'stock': 100,
                    'is_featured': True,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample products')
        )
