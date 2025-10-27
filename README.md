# Fruitables - Django E-commerce Website

A modern e-commerce website for fresh fruits and vegetables built with Django, featuring user authentication, product management, shopping cart functionality, comprehensive testing framework, and a responsive Bootstrap design.

## Features

- **User Authentication**: Login, registration, and user profile management
- **Product Management**: Categories, products with images, pricing, and inventory
- **Shopping Cart**: Add, update, and remove items from cart
- **Checkout Process**: Complete order placement with payment processing
- **Product Reviews**: Users can leave reviews and ratings
- **Search & Filter**: Search products and filter by category
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Admin Panel**: Full Django admin interface for content management
- **Comprehensive Testing**: Unit tests, automation tests, and quality management
- **Service Layer Architecture**: Clean separation of business logic

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Images**: Pillow for image processing
- **Authentication**: Django's built-in authentication system
- **Testing**: pytest, pytest-django, Selenium WebDriver
- **Quality Management**: Comprehensive QA framework with test automation

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

```bash
# If you have the project files, navigate to the project directory
cd fruitables-1.0.0
```

### Step 2: Install Dependencies

```bash
# Install all required packages
python -m pip install -r requirements.txt
```

### Step 3: Run Database Migrations

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)

```bash
# Create admin user (you'll be prompted for username and password)
python manage.py createsuperuser
```

### Step 5: Run the Development Server

```bash
# Start the development server
python manage.py runserver
```

The website will be available at `http://127.0.0.1:8000/`

## Usage

### Admin Panel

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Add categories and products through the admin interface

### User Features

1. **Registration**: Users can create new accounts
2. **Login**: Existing users can log in
3. **Browse Products**: View all products with search and filter options
4. **Shopping Cart**: Add products to cart and manage quantities
5. **User Profile**: Update personal information and view order history

## Project Structure

```
fruitables-1.0.0/
├── manage.py                  # Django management script
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
├── pytest.ini               # pytest configuration
│
├── fruitables/               # Main Django project
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
│
├── store/                    # Main app
│   ├── __init__.py
│   ├── admin.py              # Admin interface configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Database models
│   ├── forms.py              # Django forms
│   ├── views.py              # View functions
│   ├── urls.py               # App URL patterns
│   │
│   ├── services/             # Service layer (business logic)
│   │   ├── __init__.py
│   │   ├── user_service.py   # User-related business logic
│   │   ├── product_service.py # Product-related business logic
│   │   ├── cart_service.py   # Cart-related business logic
│   │   └── order_service.py  # Order-related business logic
│   │
│   └── tests/                # Testing framework
│       ├── __init__.py
│       │
│       ├── unit/             # Unit tests
│       │   ├── __init__.py
│       │   ├── test_user_service.py
│       │   ├── test_product_service.py
│       │   └── test_cart_service.py
│       │
│       └── automation/       # Automation tests
│           ├── __init__.py
│           │
│           ├── pages/        # Page Object Model
│           │   ├── __init__.py
│           │   ├── base_page.py
│           │   ├── login_page.py
│           │   ├── shop_page.py
│           │   └── checkout_page.py
│           │
│           └── tests/        # UI automation tests
│               ├── __init__.py
│               ├── test_login_ui.py
│               ├── test_add_to_cart_ui.py
│               └── test_checkout_ui.py
│
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   ├── registration/         # Authentication templates
│   │   └── login.html
│   └── store/                # App-specific templates
│       ├── home.html
│       ├── shop.html
│       ├── cart.html
│       ├── checkout.html
│       ├── product_detail.html
│       ├── profile.html
│       ├── register.html
│       ├── contact.html
│       ├── about.html
│       └── testimonial.html
│
├── static/                   # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   ├── img/
│   └── lib/
│
├── media/                    # User-uploaded files
│
├── quality/                  # Quality management
│   ├── qa_plan.md           # Quality assurance plan
│   ├── test_cases.csv       # Test cases documentation
│   ├── defect_log.csv       # Defect tracking
│   └── test_report.html     # Test execution report
│
└── README.md                 # This file
```

## Database Models

### Core Models

- **Category**: Product categories (Fruits, Vegetables, etc.)
- **Product**: Individual products with pricing and inventory
- **UserProfile**: Extended user information
- **Cart/CartItem**: Shopping cart functionality
- **Review**: Product reviews and ratings

## Testing Framework

### Test Structure

The project includes a comprehensive testing framework with multiple layers:

#### Unit Tests
- **Location**: `store/tests/unit/`
- **Coverage**: Service layer methods, model methods, utility functions
- **Tools**: pytest, pytest-django
- **Run**: `pytest store/tests/unit/`

#### Automation Tests
- **Location**: `store/tests/automation/`
- **Coverage**: UI functionality, user workflows, cross-browser testing
- **Tools**: Selenium WebDriver, pytest
- **Page Objects**: Organized in `store/tests/automation/pages/`
- **Run**: `pytest store/tests/automation/`

### Running Tests

```bash
# Run all tests
pytest

# Run unit tests only
pytest store/tests/unit/

# Run automation tests only
pytest store/tests/automation/

# Run with coverage
pytest --cov=store

# Run specific test file
pytest store/tests/unit/test_user_service.py
```

### Test Configuration

- **pytest.ini**: Main pytest configuration
- **Coverage**: Minimum 80% code coverage required
- **Markers**: Unit, integration, automation, smoke, regression tests
- **Parallel Execution**: Supported with pytest-xdist

## Quality Management

### QA Framework

The project includes a comprehensive quality assurance framework:

#### Quality Components
- **QA Plan**: `quality/qa_plan.md` - Comprehensive testing strategy
- **Test Cases**: `quality/test_cases.csv` - Detailed test case documentation
- **Defect Log**: `quality/defect_log.csv` - Defect tracking and management
- **Test Reports**: `quality/test_report.html` - Automated test execution reports

#### Quality Metrics
- **Test Coverage**: 80%+ code coverage
- **Performance**: Page load time < 3 seconds
- **Accessibility**: WCAG 2.1 AA compliance
- **Security**: OWASP Top 10 compliance
- **Browser Compatibility**: Chrome, Firefox, Safari, Edge

### Service Layer Architecture

The project follows a clean architecture pattern with service layer separation:

#### Services
- **UserService**: User management, authentication, profile operations
- **ProductService**: Product operations, search, filtering, reviews
- **CartService**: Shopping cart management, item operations
- **OrderService**: Order processing, payment handling, order management

#### Benefits
- **Separation of Concerns**: Business logic separated from views
- **Testability**: Services can be unit tested independently
- **Reusability**: Services can be used across different views
- **Maintainability**: Easier to modify and extend functionality

## Customization

### Adding New Features

1. **New Models**: Add to `store/models.py`
2. **New Views**: Add to `store/views.py`
3. **New URLs**: Add to `store/urls.py`
4. **New Templates**: Create in `templates/store/`

### Styling

- Main CSS: `static/css/style.css`
- Bootstrap customization: Modify CSS variables
- Template styling: Edit individual template files

### Configuration

- Database settings: `fruitables/settings.py`
- Static files: Configure in settings for production
- Email settings: Add SMTP configuration for contact forms

## Production Deployment

### Recommended Steps

1. **Change Database**: Use PostgreSQL or MySQL
2. **Static Files**: Configure static file serving
3. **Environment Variables**: Use python-decouple for sensitive data
4. **Security**: Update SECRET_KEY and disable DEBUG
5. **Web Server**: Use Gunicorn with Nginx

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Troubleshooting

### Common Issues

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database errors**: Check migrations with `python manage.py showmigrations`
3. **Import errors**: Ensure all packages are installed from requirements.txt
4. **Image upload issues**: Check media directory permissions

### Support

For issues and questions:
1. Check Django documentation
2. Review error messages in console
3. Verify all dependencies are installed correctly

## License

This project is based on a free HTML template and is provided as-is for educational purposes.

## Contributing

Feel free to fork this project and submit pull requests for improvements.

---

**Note**: This is a development version. For production use, ensure proper security measures, database optimization, and deployment best practices are followed.
