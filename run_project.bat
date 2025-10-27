@echo off
echo ========================================
echo    Fruitables Django E-commerce
echo ========================================
echo.
echo Activating Virtual Environment...
call venv\Scripts\activate.bat

echo.
echo Starting Django Development Server...
echo.
echo Your website will be available at:
echo http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
