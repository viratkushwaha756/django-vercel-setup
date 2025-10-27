from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Product, Review, Cart, CartItem, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, ReviewForm, ContactForm, UserLoginForm

def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    categories = Category.objects.all()[:4]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'store/home.html', context)

def shop(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'store/shop.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    reviews = product.reviews.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product_detail', slug=slug)
    else:
        review_form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'store/product_detail.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Fruitables!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'store/register.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'store/profile.html', context)

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'clear':
            cart.items.all().delete()
            messages.success(request, 'Cart cleared successfully!')
        else:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                
                if action == 'add':
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart, 
                        product=product,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                    messages.success(request, f'{product.name} added to cart!')
                
                elif action == 'update':
                    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, 'Cart updated!')
                
                elif action == 'remove':
                    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                    cart_item.delete()
                    messages.success(request, f'{product.name} removed from cart!')
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you would typically send an email
            # For now, we'll just show a success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'store/contact.html', {'form': form})

def about(request):
    return render(request, 'store/about.html')

def testimonial(request):
    return render(request, 'store/testimonial.html')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty. Please add some products first.')
        return redirect('shop')
    
    if request.method == 'POST':
        # Process checkout form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        
        # Payment information
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholder_name')
        
        # Validate required fields
        required_fields = [first_name, last_name, email, phone, address, city, state, zip_code,
                          card_number, expiry_date, cvv, cardholder_name]
        
        if not all(required_fields):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')
        
        # Process order (simplified - in real application, integrate with payment gateway)
        try:
            # Calculate totals using cart properties
            subtotal = float(cart.total_price)
            tax = float(cart.tax_amount)
            shipping = float(cart.shipping_cost)
            total = float(cart.final_total)
            
            # Create order (simplified)
            order_data = {
                'user': request.user,
                'subtotal': subtotal,
                'tax': tax,
                'shipping': shipping,
                'total': total,
                'shipping_address': f"{address}, {city}, {state} {zip_code}",
                'payment_method': 'Credit Card',
                'status': 'completed'
            }
            
            # Clear cart after successful order
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully! Thank you for your purchase.')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('checkout')
    
    context = {
        'cart': cart,
    }
    return render(request, 'store/checkout.html', context)